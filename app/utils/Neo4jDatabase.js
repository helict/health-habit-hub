import neo4j from 'neo4j-driver';
import fetch from 'node-fetch';
import { v4 as uuid } from 'uuid';

// Share the same shape as SparqlDatabase but target Neo4j

// function to translate text using LibreTranslate API
async function translate(text, from, to, config, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const response = await fetch(config.getTranslateApiEndpoint(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: text, source: from, target: to, format: 'text', alternatives: 0 }),
        signal: controller.signal
      });

      clearTimeout(timeout);

      if (response.ok) {
        const translation = await response.json();
        return translation.translatedText;
      }

      throw new Error(`Translation failed: ${response.status} ${response.statusText}`);
    } catch (error) {
      console.warn(`Translation attempt ${attempt}/${retries} failed:`, error.message);
      
      // If this is the last attempt, or it's not a connection error, return original text
      if (attempt === retries || !error.message.includes('ECONNREFUSED')) {
        console.error(`Translation service unavailable after ${retries} attempts. Returning original text.`);
        return text; // Return original text as fallback
      }
      
      // Wait before retrying (exponential backoff)
      const delay = Math.min(1000 * Math.pow(2, attempt - 1), 5000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

class ExperimentalSetting {
  id;
  description;
  task;
  group;

  constructor(setting) {
    this.id = uuid();
    this.description = setting.closedDescription ? 'closed' : 'open';
    this.task = setting.closedTask ? 'closed' : 'open';
    if (this.isClosedTaskOpenDescription()) this.group = 'Group1';
    else if (this.isClosedTaskClosedDescription()) this.group = 'Group2';
    else if (this.isOpenTaskClosedDescription()) this.group = 'Group3';
    else if (this.isOpenTaskOpenDescription()) this.group = 'Group4';
  }

  isClosedTaskClosedDescription() {
    return this.task === 'closed' && this.description === 'closed';
  }
  isClosedTaskOpenDescription() {
    return this.task === 'closed' && this.description === 'open';
  }
  isOpenTaskOpenDescription() {
    return this.task === 'open' && this.description === 'open';
  }
  isOpenTaskClosedDescription() {
    return this.task === 'open' && this.description === 'closed';
  }
}

class Donor {
  id;
  donation;
  constructor(donation) {
    this.id = uuid();
    this.donation = donation;
  }
}

class Label {
  id;
  type;
  value;
  data;
  constructor(type, value, data) {
    this.id = uuid();
    this.type = type; // 'context' | 'behavior'
    this.value = value; // label name
    this.data = data; // label text
  }
}

class Donation {
  id;
  value;
  labels;
  language;
  source;
  translation;
  habitStrength;

  constructor(value, language, labels, source, habitStrength) {
    this.id = uuid();
    this.value = value;
    this.language = language;
    this.labels = labels.map(
      (label) =>
        new Label(
          {
            TimeReference: 'context',
            PhysicalSetting: 'context',
            People: 'context',
            InternalState: 'context',
            PriorBehavior: 'context',
            Reasoning: 'context',
            Behavior: 'behavior',
          }[label.name],
          label.name,
          label.value,
        ),
    );
    this.source = source;
    const hs = parseInt(habitStrength, 10);
    this.habitStrength = Number.isFinite(hs) ? hs : 0;
  }

  hasLabels() {
    return this.labels && this.labels.length > 0;
  }

  async translate(targetLanguage, config) {
    const translatedValue = await translate(this.value, this.language, targetLanguage, config);
    const translatedLabels = this.hasLabels()
      ? await Promise.all(this.labels.map(async (label) => translate(label.data, this.language, targetLanguage, config)))
      : [];

    const labelsCopy = this.labels.map((label, index) => Object.assign({ name: label.value, value: translatedLabels[index] }));
    this.translation = new Donation(translatedValue, targetLanguage, labelsCopy, 'translation', this.habitStrength);
    return this.translation;
  }
}

class Neo4jDbClient {
  constructor(config) {
    this.config = config;
    this.driver = neo4j.driver(
      config.neo4j.uri,
      neo4j.auth.basic(config.neo4j.user, config.neo4j.password),
    );
    this.n10sConfigured = false;
  }

  _esc(str) {
    if (str == null) return '';
    return String(str)
      .replace(/\\/g, "\\\\")
      .replace(/\"/g, '\\"')
      .replace(/\n/g, "\\n")
      .replace(/\r/g, "\\r");
  }

  async close() {
    await this.driver.close();
  }

  async ensureN10sConfigured() {
    if (this.n10sConfigured) return;
    const session = this.driver.session({ defaultAccessMode: neo4j.session.WRITE });
    try {
      // Ensure required uniqueness constraint for n10s
      try {
        await session.run(
          `CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS FOR (r:Resource) REQUIRE r.uri IS UNIQUE`
        );
      } catch (e) {
        // console.warn('n10s: constraint creation warning:', e.message);
      }

      // If graph config exists this will throw; we'll ignore and continue
      await session.run(
        `CALL n10s.graphconfig.init({ handleVocabUris: 'SHORTEN', keepLangTag: true, handleMultival: 'ARRAY' })`
      );
    } catch (e) {
      // If already configured, that's fine
    }
    // Ensure namespace prefix for hhh is registered for cleaner mapping
    try {
      await session.run(`CALL n10s.nsprefixes.add($prefix,$ns)` , { prefix: 'hhh', ns: 'http://example.com/hhh#' });
    } catch (e) {
      // ignore
    }

    // Import only the schema (classes/properties) to avoid example individuals.
    // We prefer schema.ttl; only if it's missing, we fall back to Ontology.ttl (which may include examples).
    try {
      const resSchema = await session.run(
        `CALL n10s.rdf.import.fetch($url,'Turtle')`,
        { url: 'file:///import/schema.ttl' }
      );
      // console.log('n10s: imported schema.ttl', resSchema.summary?.counters ?? '');
    } catch (e1) {
      // console.warn('n10s: schema.ttl import failed, trying Ontology.ttl:', e1.message);
      try {
        const resOnt = await session.run(
          `CALL n10s.rdf.import.fetch($url,'Turtle')`,
          { url: 'file:///import/Ontology.ttl' }
        );
        // console.log('n10s: imported Ontology.ttl', resOnt.summary?.counters ?? '');
      } catch (e2) {
        // console.warn('n10s: Ontology.ttl import also failed:', e2.message);
      }
    } finally {
      await session.close();
    }
    this.n10sConfigured = true;
  }

  async insertDonateData(data, userId) {
    const NORMALIZE_LANG = 'en';
    await this.ensureN10sConfigured();

    const mustTranslate = !data.language.toLowerCase().startsWith(NORMALIZE_LANG);
    const experimentalSetting = new ExperimentalSetting(data.experimentGroup);
    const donation = new Donation(
      data.inputValue,
      data.language,
      data.contexts,
      userId,
      parseInt(data.habitStrength, 10),
    );
    const donor = new Donor(donation);
    const timestamp = new Date().toISOString();

    if (mustTranslate) {
      await donation.translate(NORMALIZE_LANG, this.config);
    }

    // Build Turtle payload aligned with the RDF schema (hhh namespace)
    const parts = this._buildDonationTurtle(donation, experimentalSetting, userId, timestamp);

    const session = this.driver.session({ defaultAccessMode: neo4j.session.WRITE });
    try {
      await this._importTurtle(session, parts.prefixes + parts.experimentalSettingTriples + parts.habitTriples + parts.donorTriples, 'base+habit');
      if (parts.contextTriples) await this._importTurtle(session, parts.prefixes + parts.contextTriples, 'contexts');
      if (parts.behaviorTriples || parts.habitBehaviorLinks) await this._importTurtle(session, parts.prefixes + parts.behaviorTriples + parts.habitBehaviorLinks, 'behaviors+links');
      if (parts.translationTriples) await this._importTurtle(session, parts.prefixes + parts.translationTriples, 'translations');
    } finally {
      await session.close();
    }
  }

  async _importTurtle(session, payload, label) {
    try {
      const res = await session.run(`CALL n10s.rdf.import.inline($payload, 'Turtle')`, { payload });
      const first = res.records?.[0]?.toObject?.() ?? {};
      const status = first.terminationStatus || first['terminationStatus'] || 'UNKNOWN';
      /*
      console.log(`n10s inline import [${label}]:`, {
        terminationStatus: status,
        triplesLoaded: first.triplesLoaded,
        triplesParsed: first.triplesParsed,
        namespaces: first.namespaces,
      });
      */
      // console.debug(`n10s inline raw [${label}]:`, first);
      if (status !== 'OK') {
        const preview = await session.run(`CALL n10s.rdf.preview.inline($payload, 'Turtle')`, { payload });
        const info = preview.records?.[0]?.toObject?.() ?? {};
        // console.warn(`n10s preview [${label}]:`, info);
        // console.debug(`Turtle payload [${label}] (first 1200 chars):`, payload.slice(0, 1200));
      }
      return status === 'OK';
    } catch (e) {
      // console.error(`n10s inline import failed [${label}]:`, e.message);
      // console.debug(`First 400 chars of payload [${label}]:`, payload.slice(0, 400));
      throw e;
    }
  }

  _buildDonationTurtle(donation, experimentalSetting, userId, timestamp) {
    const prefixes = `
@prefix hhh: <http://example.com/hhh#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
`;

    const iri = (local) => `<http://example.com/hhh#${local}>`;
    const donorId = uuid();

    const habitTriples = `
${iri(`Habit-${donation.id}`)} rdf:type owl:NamedIndividual , hhh:Habit ;
  hhh:habitStrength "${donation.habitStrength}"^^xsd:integer ;
  hhh:id "${donation.id}"^^xsd:string ;
  hhh:language "${this._esc(donation.language)}" ;
  hhh:source "${this._esc(donation.source)}"^^xsd:string ;
  hhh:value "${this._esc(donation.value)}" .
`;

    const experimentalSettingTriples = `
${iri(`ExperimentalSetting-${experimentalSetting.id}`)} rdf:type owl:NamedIndividual , hhh:${experimentalSetting.group} .
`;

    const donorTriples = `
${iri(`Donor-${donorId}`)} rdf:type owl:NamedIndividual , hhh:Donor ;
  hhh:donates ${iri(`Habit-${donation.id}`)} ;
  hhh:userId "${userId}"^^xsd:string ;
  hhh:timestamp "${timestamp}"^^xsd:dateTime ;
  hhh:id "${donorId}"^^xsd:string .
`;

    const contexts = donation.labels.filter((l) => l.type === 'context');
    const behaviors = donation.labels.filter((l) => l.type === 'behavior');

    const contextTriples = contexts
      .map((c) => `
${iri(`Context-${c.id}`)} rdf:type owl:NamedIndividual , hhh:${c.value} ;
  hhh:partOf ${iri(`ExperimentalSetting-${experimentalSetting.id}`)} ;
  hhh:id "${c.id}"^^xsd:string ;
  hhh:language "${this._esc(donation.language)}" ;
  hhh:source "${this._esc(donation.source)}"^^xsd:string ;
  hhh:value "${this._esc(c.data)}" .
`)
      .join('');

    const behaviorTriples = behaviors
      .map((b) => {
        const ctxList = contexts.map((c) => iri(`Context-${c.id}`)).join(' , ');
        const hasCtx = ctxList ? `\n  hhh:hasContext ${ctxList} ;` : '';
        return `
${iri(`Behavior-${b.id}`)} rdf:type owl:NamedIndividual , hhh:Behavior ;${hasCtx}
  hhh:partOf ${iri(`ExperimentalSetting-${experimentalSetting.id}`)} ;
  hhh:id "${b.id}"^^xsd:string ;
  hhh:language "${this._esc(donation.language)}" ;
  hhh:source "${this._esc(donation.source)}"^^xsd:string ;
  hhh:value "${this._esc(b.data)}" .
`;
      })
      .join('');

    // Link habit to behaviors if present
    const habitBehaviorLinks = behaviors.length
      ? `${iri(`Habit-${donation.id}`)} hhh:hasBehavior ${behaviors
          .map((b) => iri(`Behavior-${b.id}`))
          .join(' , ')} .
`
      : '';

    let translationTriples = '';
    if (donation.translation) {
      const t = donation.translation;

      translationTriples += `
${iri(`Habit-${donation.id}`)} hhh:hasTranslation ${iri(`Habit-${t.id}`)} .
${iri(`Habit-${t.id}`)} rdf:type owl:NamedIndividual , hhh:Habit ;
  hhh:habitStrength "${t.habitStrength}"^^xsd:integer ;
  hhh:id "${t.id}"^^xsd:string ;
  hhh:language "${this._esc(t.language)}" ;
  hhh:source "${this._esc(t.source)}"^^xsd:string ;
  hhh:value "${this._esc(t.value)}" .
`;

      const origByValue = new Map(donation.labels.map((l) => [l.value, l]));

      const tContexts = t.labels.filter((l) => l.name !== 'Behavior');
      const tBehaviors = t.labels.filter((l) => l.name === 'Behavior');

      translationTriples += tContexts
        .map((tc) => {
          const orig = origByValue.get(tc.name);
          const tid = uuid();
          return `
${iri(`Context-${tid}`)} rdf:type owl:NamedIndividual , hhh:${tc.name} ;
  hhh:partOf ${iri(`ExperimentalSetting-${experimentalSetting.id}`)} ;
  hhh:id "${tid}"^^xsd:string ;
  hhh:language "${this._esc(t.language)}" ;
  hhh:source "${this._esc(t.source)}"^^xsd:string ;
  hhh:value "${this._esc(tc.value)}" .
${orig ? `${iri(`Context-${orig.id}`)} hhh:hasTranslation ${iri(`Context-${tid}`)} .` : ''}
`;
        })
        .join('');

      translationTriples += tBehaviors
        .map((tb) => {
          const orig = origByValue.get(tb.name);
          const tid = uuid();
          return `
${iri(`Behavior-${tid}`)} rdf:type owl:NamedIndividual , hhh:Behavior ;
  hhh:partOf ${iri(`ExperimentalSetting-${experimentalSetting.id}`)} ;
  hhh:id "${tid}"^^xsd:string ;
  hhh:language "${this._esc(t.language)}" ;
  hhh:source "${this._esc(t.source)}"^^xsd:string ;
  hhh:value "${this._esc(tb.value)}" .
${orig ? `${iri(`Behavior-${orig.id}`)} hhh:hasTranslation ${iri(`Behavior-${tid}`)} .` : ''}
`;
        })
        .join('');
    }

    return {
      prefixes,
      experimentalSettingTriples,
      habitTriples,
      donorTriples,
      contextTriples,
      behaviorTriples,
      habitBehaviorLinks,
      translationTriples,
    };
  }
}

export { Neo4jDbClient };
