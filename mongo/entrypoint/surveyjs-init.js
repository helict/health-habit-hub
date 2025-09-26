db = new Mongo().getDB("surveyjs");

db.createCollection("surveys");
console.log("Collection 'surveys' created.");
db.surveys.insert([
{
  "id": "1", 
  "completedHtml": {
    "default": "<h4>Thank you for your participation!</h4>",
    "de": "<h4>Vielen Dank für Ihre Teilnahme!</h4>",
    "ja": "<h4>ご参加いただきありがとうございます！</h4>"
  },
  "showProgressBar": true,
  "progressBarLocation": "top",
  "pages": [
    {
      "name": "demographics",
      "title": {
        "default": "About You",
        "de": "Über Sie",
        "ja": "あなたについて"
      },
      "description": {
        "default": "Please provide some information about yourself.",
        "de": "Bitte machen Sie einige Angaben zu Ihrer Person.",
        "ja": "ご自身に関する情報をご提供ください。"
      },
      "elements": [
        {
          "type": "radiogroup",
          "name": "gender",
          "title": {
            "default": "Gender",
            "de": "Geschlecht",
            "ja": "性別"
          },
          "description": {
            "default": "Please select your gender.",
            "de": "Bitte wählen Sie Ihr Geschlecht.",
            "ja": "性別を選択してください。"
          },
          "choices": [
            {
              "value": "männlich",
              "text": {
                "default": "Male",
                "de": "Männlich",
                "ja": "男性"
              }
            },
            {
              "value": "weiblich",
              "text": {
                "default": "Female",
                "de": "Weiblich",
                "ja": "女性"
              }
            },
            {
              "value": "divers",
              "text": {
                "default": "Other",
                "de": "Divers",
                "ja": "その他"
              }
            }
          ]
        },
        {
          "type": "dropdown",
          "name": "country",
          "title": {
            "default": "Country of Origin",
            "de": "Herkunft",
            "ja": "出身国"
          },
          "description": {
            "default": "Please specify your country of origin.",
            "de": "Geben Sie Ihr Herkunftsland an.",
            "ja": "出身国を選択してください。"
          },
          "choicesByUrl": {
            "url": "https://restcountries.com/v2/all?fields=name",
            "valueName": "name",
            "titleName": "name"
          },
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "education",
          "title": {
            "default": "Highest Education",
            "de": "Schulabschluss",
            "ja": "学歴"
          },
          "description": {
            "default": "Please select your highest level of education.",
            "de": "Wählen Sie Ihren höchsten Schulabschluss.",
            "ja": "最終学歴を選択してください。"
          },
          "choices": [
            {
              "value": "abitur",
              "text": {
                "default": "university entrance diploma",
                "de": "Abitur",
                "ja": "アビトゥーア"
              }
            },
            {
              "value": "fachabitur",
              "text": {
                "default": "vocational diploma",
                "de": "Fachabitur",
                "ja": "ファッハアビトゥーア"
              }
            },
            {
              "value": "Lower Secondary School Certificate",
              "text": {
                "default": "Hauptschulabschluss",
                "de": "Hauptschulabschluss",
                "ja": "ハウプトシューレ卒業"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "text",
          "name": "age",
          "title": {
            "default": "Age",
            "de": "Alter",
            "ja": "年齢"
          },
          "description": {
            "default": "Please enter your age.",
            "de": "Geben Sie Ihr Alter an.",
            "ja": "年齢を入力してください。"
          },
          "validators": [
            {
              "type": "numeric",
              "minValue": 0,
              "maxValue": 122
            }
          ],
          "inputType": "number",
          "placeholder": {
            "default": "Please enter",
            "de": "Bitte eingeben",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "weight",
          "title": {
            "default": "Weight Category",
            "de": "Gewichtsklasse",
            "ja": "体重カテゴリ"
          },
          "description": {
            "default": "Please select your weight category.",
            "de": "Wählen Sie Ihre Gewichtsklasse.",
            "ja": "体重カテゴリを選択してください。"
          },
          "choices": [
            {
              "value": "untergewichtig",
              "text": {
                "default": "Underweight",
                "de": "Untergewichtig",
                "ja": "低体重"
              }
            },
            {
              "value": "normalgewichtig",
              "text": {
                "default": "Normal weight",
                "de": "Normalgewichtig",
                "ja": "標準体重"
              }
            },
            {
              "value": "übergewichtig",
              "text": {
                "default": "Overweight",
                "de": "Übergewichtig",
                "ja": "過体重"
              }
            },
            {
              "value": "stark-übergewichtig",
              "text": {
                "default": "Obese",
                "de": "Stark übergewichtig",
                "ja": "肥満"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "employment_context",
          "title": {
            "default": "Employment Status",
            "de": "Berufliche Situation",
            "ja": "雇用状況"
          },
          "description": {
            "default": "Please select your employment status.",
            "de": "Wählen Sie Ihre berufliche Situation.",
            "ja": "雇用状況を選択してください。"
          },
          "choices": [
            {
              "value": "im-studium",
              "text": {
                "default": "Student",
                "de": "Im Studium",
                "ja": "学生"
              }
            },
            {
              "value": "in-ausbildung",
              "text": {
                "default": "In vocational training",
                "de": "In Ausbildung",
                "ja": "職業訓練中"
              }
            },
            {
              "value": "angestellt-vollzeit",
              "text": {
                "default": "Employed full‑time",
                "de": "Vollzeit angestellt",
                "ja": "フルタイム雇用"
              }
            },
            {
              "value": "angestellt-teilzeit",
              "text": {
                "default": "Employed part‑time",
                "de": "Teilzeit angestellt",
                "ja": "パートタイム雇用"
              }
            },
            {
              "value": "selbstständig",
              "text": {
                "default": "Self‑employed",
                "de": "Selbstständig",
                "ja": "自営業"
              }
            },
            {
              "value": "arbeitssuchend",
              "text": {
                "default": "Unemployed",
                "de": "Arbeitssuchend",
                "ja": "失業中"
              }
            },
            {
              "value": "in-rente",
              "text": {
                "default": "Retired",
                "de": "In Rente",
                "ja": "退職"
              }
            },
            {
              "value": "hausarbeit-familienpflege",
              "text": {
                "default": "Housework / Family care",
                "de": "Hausarbeit / Familienpflege",
                "ja": "家事／家族ケア"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "working_hours",
          "title": {
            "default": "Working Hours",
            "de": "Arbeitszeiten",
            "ja": "勤務時間"
          },
          "description": {
            "default": "Please select your working hours system.",
            "de": "Wählen Sie Ihr Arbeitszeitsystem.",
            "ja": "勤務時間体系を選択してください。"
          },
          "choices": [
            {
              "value": "schichtsystem-mit-nachtschicht",
              "text": {
                "default": "Shift with night shifts",
                "de": "Schichtsystem mit Nachtschicht",
                "ja": "夜勤ありシフト制"
              }
            },
            {
              "value": "schichtsystem-ohne-nachtschichten",
              "text": {
                "default": "Shift without night shifts",
                "de": "Schichtsystem ohne Nachtschicht",
                "ja": "夜勤なしシフト制"
              }
            },
            {
              "value": "wochenende-oft-im-dienst",
              "text": {
                "default": "Often on duty weekends",
                "de": "Oft am Wochenende im Dienst",
                "ja": "週末よく勤務"
              }
            },
            {
              "value": "wochenende-meistens-frei",
              "text": {
                "default": "Mostly free on weekends",
                "de": "Meistens am Wochenende frei",
                "ja": "週末は主に休み"
              }
            },
            {
              "value": "wochenende-immer-frei",
              "text": {
                "default": "Always free on weekends",
                "de": "Immer am Wochenende frei",
                "ja": "週末は常に休み"
              }
            },
            {
              "value": "flexible-arbeitszeiten",
              "text": {
                "default": "Flexible working hours",
                "de": "Flexible Arbeitszeiten",
                "ja": "フレックスタイム"
              }
            },
            {
              "value": "unflexible-arbeitszeiten",
              "text": {
                "default": "Fixed working hours",
                "de": "Unflexible Arbeitszeiten",
                "ja": "固定勤務時間"
              }
            },
            {
              "value": "homeoffice",
              "text": {
                "default": "Home office",
                "de": "Homeoffice",
                "ja": "在宅勤務"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "commute_mode",
          "title": {
            "default": "Commute Mode",
            "de": "Arbeitsweg",
            "ja": "通勤手段"
          },
          "description": {
            "default": "How do you commute to work?",
            "de": "Wie kommen Sie zur Arbeit?",
            "ja": "通勤手段を選択してください。"
          },
          "choices": [
            {
              "value": "autofahrt",
              "text": {
                "default": "By car",
                "de": "Autofahrt",
                "ja": "自動車"
              }
            },
            {
              "value": "fußweg",
              "text": {
                "default": "On foot",
                "de": "Fußweg",
                "ja": "徒歩"
              }
            },
            {
              "value": "fahrradfahrt",
              "text": {
                "default": "By bicycle",
                "de": "Fahrradfahrt",
                "ja": "自転車"
              }
            },
            {
              "value": "öffentliche-verkehrsmittel",
              "text": {
                "default": "Public transport",
                "de": "Öffentliche Verkehrsmittel",
                "ja": "公共交通機関"
              }
            },
            {
              "value": "motorradfahrt",
              "text": {
                "default": "By motorcycle",
                "de": "Motorradfahrt",
                "ja": "バイク"
              }
            },
            {
              "value": "mitfahrgelegenheit",
              "text": {
                "default": "Carpooling",
                "de": "Mitfahrgelegenheit",
                "ja": "相乗り"
              }
            },
            {
              "value": "telecommuting",
              "text": {
                "default": "Telecommuting",
                "de": "Telecommuting",
                "ja": "テレコミューティング"
              }
            },
            {
              "value": "other",
              "text": {
                "default": "Other",
                "de": "Sonstiges",
                "ja": "その他"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "personal_context",
          "title": {
            "default": "Personal Situation",
            "de": "Private Situation",
            "ja": "プライベート状況"
          },
          "description": {
            "default": "Please select your personal situation.",
            "de": "Wählen Sie Ihre private Situation.",
            "ja": "プライベート状況を選択してください。"
          },
          "choices": [
            {
              "value": "partnerschaft-ohne-kind",
              "text": {
                "default": "Partnership without child",
                "de": "Partnerschaft ohne Kind",
                "ja": "子供なしパートナーシップ"
              }
            },
            {
              "value": "partnerschaft-mit-kind",
              "text": {
                "default": "Partnership with child",
                "de": "Partnerschaft mit Kind",
                "ja": "子供ありパートナーシップ"
              }
            },
            {
              "value": "alleinerziehend",
              "text": {
                "default": "Single parent",
                "de": "Alleinerziehend",
                "ja": "シングル親"
              }
            },
            {
              "value": "single-ohne-kind",
              "text": {
                "default": "Single without child",
                "de": "Single ohne Kind",
                "ja": "子供なしシングル"
              }
            },
            {
              "value": "getrennt-lebend-partnerschaft-kind",
              "text": {
                "default": "Separated with partner & child",
                "de": "Getrennt lebend mit Partner & Kind",
                "ja": "離別・パートナー＆子供あり"
              }
            },
            {
              "value": "getrennt-lebend-single-kind",
              "text": {
                "default": "Separated single with child",
                "de": "Getrennt lebend als Single mit Kind",
                "ja": "離別・シングル＆子供あり"
              }
            },
            {
              "value": "getrennt-lebend-single-ohne-kind",
              "text": {
                "default": "Separated single without child",
                "de": "Getrennt lebend als Single ohne Kind",
                "ja": "離別・シングル＆子供なし"
              }
            },
            {
              "value": "andere-familienkonstellation",
              "text": {
                "default": "Other family constellation",
                "de": "Andere Familienkonstellation",
                "ja": "その他の家族構成"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "available_time",
          "title": {
            "default": "Available Time per Day",
            "de": "Verfügbare Zeit pro Tag",
            "ja": "1日あたりの利用可能時間"
          },
          "description": {
            "default": "How much time is available to you daily?",
            "de": "Wie viel Zeit steht Ihnen täglich zur Verfügung?",
            "ja": "1日に利用できる時間を選択してください。"
          },
          "choices": [
            {
              "value": "mehr-als-3-stunden",
              "text": {
                "default": "More than 3 hours",
                "de": "Mehr als 3 Stunden",
                "ja": "3時間以上"
              }
            },
            {
              "value": "2-3-stunden",
              "text": {
                "default": "2–3 hours",
                "de": "2–3 Stunden",
                "ja": "2～3時間"
              }
            },
            {
              "value": "1-2-stunden",
              "text": {
                "default": "1–2 hours",
                "de": "1–2 Stunden",
                "ja": "1～2時間"
              }
            },
            {
              "value": "0-5-1-stunde",
              "text": {
                "default": "0.5–1 hour",
                "de": "0,5–1 Stunde",
                "ja": "0.5～1時間"
              }
            },
            {
              "value": "weniger-als-0-5-stunden",
              "text": {
                "default": "Less than 0.5 hour",
                "de": "Weniger als 0,5 Stunden",
                "ja": "0.5時間未満"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "relationship_context",
          "title": {
            "default": "Partner’s Health Context",
            "de": "Beziehungskontext",
            "ja": "パートナーの健康状況"
          },
          "description": {
            "default": "Please select your partner’s health context.",
            "de": "Wählen Sie den Gesundheitskontext Ihres Partners.",
            "ja": "パートナーの健康状況を選択してください。"
          },
          "choices": [
            {
              "value": "gesundheitsbewusster-partner",
              "text": {
                "default": "Health‑conscious partner",
                "de": "Gesundheitsbewusster Partner",
                "ja": "健康志向のパートナー"
              }
            },
            {
              "value": "mäßig-gesundheitsbewusster-partner",
              "text": {
                "default": "Moderately health‑conscious partner",
                "de": "Mäßig gesundheitsbewusster Partner",
                "ja": "やや健康志向のパートナー"
              }
            },
            {
              "value": "unterstützender-partner",
              "text": {
                "default": "Supportive partner",
                "de": "Unterstützender Partner",
                "ja": "サポートしてくれるパートナー"
              }
            },
            {
              "value": "wenig-gesundheitsbewusster-partner",
              "text": {
                "default": "Not very health‑conscious partner",
                "de": "Wenig gesundheitsbewusster Partner",
                "ja": "あまり健康志向でないパートナー"
              }
            },
            {
              "value": "überwiegend-inaktiver-partner",
              "text": {
                "default": "Mostly inactive partner",
                "de": "Überwiegend inaktiver Partner",
                "ja": "主に不活発なパートナー"
              }
            },
            {
              "value": "kein-partner",
              "text": {
                "default": "No partner",
                "de": "Kein Partner",
                "ja": "パートナーなし"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        },
        {
          "type": "dropdown",
          "name": "pet_influence",
          "title": {
            "default": "Pets Influence",
            "de": "Haustiere",
            "ja": "ペットの影響"
          },
          "description": {
            "default": "Please select how pets influence your activity.",
            "de": "Wählen Sie den Einfluss von Haustieren auf Ihre Aktivität.",
            "ja": "ペットが活動に与える影響を選択してください。"
          },
          "choices": [
            {
              "value": "regelmäßige-bewegung",
              "text": {
                "default": "Regular exercise thanks to pet",
                "de": "Regelmäßige Bewegung durch Haustier",
                "ja": "ペットのおかげで定期的に運動"
              }
            },
            {
              "value": "mehr-aktivität-im-alltag",
              "text": {
                "default": "More daily activity",
                "de": "Mehr Aktivität im Alltag",
                "ja": "日常での活動量増加"
              }
            },
            {
              "value": "kein-einfluss",
              "text": {
                "default": "No influence",
                "de": "Kein Einfluss",
                "ja": "影響なし"
              }
            },
            {
              "value": "keine-haustiere",
              "text": {
                "default": "No pets",
                "de": "Keine Haustiere",
                "ja": "ペットなし"
              }
            }
          ],
          "placeholder": {
            "default": "Please select",
            "de": "Bitte auswählen",
            "ja": "選択してください"
          }
        }
      ]
    },
    {
      "name": "sus",
      "title": {
        "default": "System Usability",
        "de": "System-Benutzerfreundlichkeit",
        "ja": "システムの使いやすさ"
      },
      "description": {
        "default": "For each of the following statements, please select a point on the scale to indicate the extent to which you agree or disagree.",
        "de": "Bitte wählen Sie für jede der folgenden Aussagen einen Punkt auf der Skala, um anzugeben, inwieweit Sie zustimmen oder nicht zustimmen.",
        "ja": "以下の各項目について、同意するかしないかの度合いをスケール上で選択してください。"
      },
      "elements": [
        {
          "type": "rating",
          "name": "sus_q1",
          "title": {
            "default": "I think that I would like to use this system frequently.",
            "de": "Ich denke, dass ich dieses Produkt häufig verwenden möchte.",
            "ja": "私はこのシステムを頻繁に使いたいと思う。"

          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q2",
          "title": {
            "default": "I found the system unnecessarily complex.",
            "de": "Ich fand das Produkt unnötig komplex.",
            "ja": "このシステムは不必要に複雑だと思う。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q3",
          "title": {
            "default": "I thought the system was easy to use.",
            "de": "Ich dachte, das Produkt war einfach zu bedienen.",
            "ja": "このシステムは使いやすいと感じる。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q4",
          "title": {
            "default": "I think that I would need the support of a technical person to be able to use this system.",
            "de": "Ich denke, dass ich die Unterstützung einer technischen Person brauche, um dieses Produkt nutzen zu können.",
            "ja": "このシステムを使うには、専門的なサポートが必要だと思う。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q5",
          "title": {
            "default": "I found the various functions in this system were well integrated.",
            "de": "Ich fand, die verschiedenen Funktionen in diesem Produkt waren gut integriert.",
            "ja": "このシステムの機能はよく統合されていると感じる。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q6",
          "title": {
            "default": "I thought there was too much inconsistency in this system.",
            "de": "Ich dachte, dass dieses Produkt nicht konsistent genug war.",
            "ja": "このシステムには一貫性が欠けている部分があると思う。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q7",
          "title": {
            "default": "I would imagine that most people would learn to use this system very quickly.",
            "de": "Ich würde mir vorstellen, dass die meisten Leute sehr schnell lernen würden, dieses Produkt zu benutzen.",
            "ja": "多くの人はこのシステムをすぐに使えるようになると思う。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q8",
          "title": {
            "default": "I found the system very cumbersome to use.",
            "de": "Ich fand dieses Produkt sehr umständlich zu benutzen.",
            "ja": "このシステムを使う前に多くのことを学ぶ必要があると思う。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q9",
          "title": {
            "default": "I felt very confident using the system.",
            "de": "Ich habe mich sehr selbstsicher gefühlt, dieses Produkt zu verwenden.",
            "ja": "このシステムを使っていると、自信を持って操作できる。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        },
        {
          "type": "rating",
          "name": "sus_q10",
          "title": {
            "default": "I needed to learn a lot of things before I could get going with this system.",
            "de": "Ich musste eine Menge Dinge lernen, bevor ich mit diesem Produkt loslegen konnte.",
            "ja": "このシステムの利用にあたって、戸惑うことが多かった。"
          },
          "minRateDescription": {
            "default": "Strongly disagree",
            "de": "Stimme überhaupt nicht zu",
            "ja": "全くそう思わない"
          },
          "maxRateDescription": {
            "default": "Strongly agree",
            "de": "Stimme voll und ganz zu",
            "ja": "非常にそう思う"
          }
        }
      ]
    },
    {
      "name": "semantic",
      "title": {
        "default": "User Experience",
        "de": "Benutzererfahrung",
        "ja": "ユーザーエクスペリエンス"
      },
      "description": {
        "default": "Please rate your experience with the system on the following scales.",
        "de": "Bitte bewerten Sie Ihre Erfahrung mit dem System auf den folgenden Skalen.",
        "ja": "以下の尺度でシステムのご利用体験を評価してください。"
      },
      "elements": [
        {
          "type": "rating",
          "name": "annoying_enjoyable",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "annoying",
            "de": "unerfreulich",
            "ja": "楽しくない"
          },
          "maxRateDescription": {
            "default": "enjoyable",
            "de": "erfreulich",
            "ja": "楽しい"
          }
        },
        {
          "type": "rating",
          "name": "not_understandable_understandable",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "not understandable",
            "de": "unverständlich",
            "ja": "わかりにくい"
          },
          "maxRateDescription": {
            "default": "understandable",
            "de": "verständlich",
            "ja": "わかりやすい"
          }
        },
        {
          "type": "rating",
          "name": "creative_dull",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "creative",
            "de": "kreativ",
            "ja": "創造的"
          },
          "maxRateDescription": {
            "default": "dull",
            "de": "phantasielos",
            "ja": "創造的でない"
          }
        },
        {
          "type": "rating",
          "name": "easy_to_learn_difficult_to_learn",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "easy to learn",
            "de": "leicht zu lernen",
            "ja": "覚えやすい"
          },
          "maxRateDescription": {
            "default": "difficult to learn",
            "de": "schwer zu lernen",
            "ja": "覚えにくい"
          }
        },
        {
          "type": "rating",
          "name": "valuable_inferior",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "valuable",
            "de": "wertvoll",
            "ja": "価値がある"
          },
          "maxRateDescription": {
            "default": "inferior",
            "de": "minderwertig",
            "ja": "価値がない"
          }
        },
        {
          "type": "rating",
          "name": "boring_exciting",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "boring",
            "de": "langweilig",
            "ja": "退屈だ"
          },
          "maxRateDescription": {
            "default": "exciting",
            "de": "spannend",
            "ja": "エキサイティングだ"
          }
        },
        {
          "type": "rating",
          "name": "not_interesting_interesting",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "not interesting",
            "de": "uninteressant",
            "ja": "おもしろくない"
          },
          "maxRateDescription": {
            "default": "interesting",
            "de": "interessant",
            "ja": "おもしろい"
          }
        },
        {
          "type": "rating",
          "name": "unpredictable_predictable",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "unpredictable",
            "de": "unberechenbar",
            "ja": "予想がつかない"
          },
          "maxRateDescription": {
            "default": "predictable",
            "de": "voraussagbar",
            "ja": "予想がつきやすい"
          }
        },
        {
          "type": "rating",
          "name": "fast_slow",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "fast",
            "de": "schnell",
            "ja": "速い"
          },
          "maxRateDescription": {
            "default": "slow",
            "de": "langsam",
            "ja": "遅い"
          }
        },
        {
          "type": "rating",
          "name": "inventive_conventional",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "inventive",
            "de": "originell",
            "ja": "独特だ"
          },
          "maxRateDescription": {
            "default": "conventional",
            "de": "konventionell",
            "ja": "従来どおり"
          }
        },
        {
          "type": "rating",
          "name": "obstructive_supportive",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "obstructive",
            "de": "behindernd",
            "ja": "妨げになる"
          },
          "maxRateDescription": {
            "default": "supportive",
            "de": "unterstützend",
            "ja": "助けられる"
          }
        },
        {
          "type": "rating",
          "name": "good_bad",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "good",
            "de": "gut",
            "ja": "良い"
          },
          "maxRateDescription": {
            "default": "bad",
            "de": "schlecht",
            "ja": "悪い"
          }
        },
        {
          "type": "rating",
          "name": "complicated_easy",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "complicated",
            "de": "kompliziert",
            "ja": "複雑"
          },
          "maxRateDescription": {
            "default": "easy",
            "de": "einfach",
            "ja": "簡単"
          }
        },
        {
          "type": "rating",
          "name": "unlikable_pleasing",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "unlikable",
            "de": "abstoßend",
            "ja": "嫌いだ"
          },
          "maxRateDescription": {
            "default": "pleasing",
            "de": "anziehend",
            "ja": "好きだ"
          }
        },
        {
          "type": "rating",
          "name": "usual_leading_edge",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "usual",
            "de": "herkömmlich",
            "ja": "普通"
          },
          "maxRateDescription": {
            "default": "leading edge",
            "de": "neuartig",
            "ja": "斬新的"
          }
        },
        {
          "type": "rating",
          "name": "unpleasant_pleasant",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "unpleasant",
            "de": "unangenehm",
            "ja": "嬉しくない"
          },
          "maxRateDescription": {
            "default": "pleasant",
            "de": "angenehm",
            "ja": "嬉しい"
          }
        },
        {
          "type": "rating",
          "name": "secure_not_secure",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "secure",
            "de": "sicher",
            "ja": "安全だ"
          },
          "maxRateDescription": {
            "default": "not secure",
            "de": "unsicher",
            "ja": "安全でない"
          }
        },
        {
          "type": "rating",
          "name": "motivating_demotivating",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "motivating",
            "de": "aktivierend",
            "ja": "モチベーションを高める"
          },
          "maxRateDescription": {
            "default": "demotivating",
            "de": "einschläfernd",
            "ja": "モチベーションを下げる"
          }
        },
        {
          "type": "rating",
          "name": "meets_expectations_does_not_meet_expectations",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "meets expectations",
            "de": "erwartungskonform",
            "ja": "期待に合う"
          },
          "maxRateDescription": {
            "default": "does not meet expectations",
            "de": "nicht erwartungskonform",
            "ja": "期待に合わない"
          }
        },
        {
          "type": "rating",
          "name": "inefficient_efficient",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "inefficient",
            "de": "ineffizient",
            "ja": "効率が悪い"
          },
          "maxRateDescription": {
            "default": "efficient",
            "de": "effizient",
            "ja": "効率が良い"
          }
        },
        {
          "type": "rating",
          "name": "clear_confusing",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "clear",
            "de": "übersichtlich",
            "ja": "すっきりしている"
          },
          "maxRateDescription": {
            "default": "confusing",
            "de": "verwirrend",
            "ja": "ごちゃごちゃしている"
          }
        },
        {
          "type": "rating",
          "name": "impractical_practical",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "impractical",
            "de": "unpragmatisch",
            "ja": "実用的でない"
          },
          "maxRateDescription": {
            "default": "practical",
            "de": "pragmatisch",
            "ja": "実用的だ"
          }
        },
        {
          "type": "rating",
          "name": "organized_cluttered",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "organized",
            "de": "aufgeräumt",
            "ja": "整理されている"
          },
          "maxRateDescription": {
            "default": "cluttered",
            "de": "überladen",
            "ja": "整理されていない"
          }
        },
        {
          "type": "rating",
          "name": "attractive_unattractive",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "attractive",
            "de": "attraktiv",
            "ja": "魅力がある"
          },
          "maxRateDescription": {
            "default": "unattractive",
            "de": "unattraktiv",
            "ja": "魅力がない"
          }
        },
        {
          "type": "rating",
          "name": "friendly_unfriendly",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "friendly",
            "de": "sympathisch",
            "ja": "感じがいい"
          },
          "maxRateDescription": {
            "default": "unfriendly",
            "de": "unsympathisch",
            "ja": "感じが悪い"
          }
        },
        {
          "type": "rating",
          "name": "conservative_innovative",
          "titleLocation": "hidden",
          "rateCount": 7,
          "rateMax": 7,
          "minRateDescription": {
            "default": "conservative",
            "de": "konservativ",
            "ja": "保守的"
          },
          "maxRateDescription": {
            "default": "innovative",
            "de": "innovativ",
            "ja": "革新的"
          }
        }
      ]
    }
  ]
}

]);

db.createCollection("results");
db.results.insert([
    { id: 1, postid: "1", json: { "Quality": { "affordable": "5", "better then others": "5", "does what it claims": "5", "easy to use": "5" }, "satisfaction": 5, "recommend friends": 5, "suggestions": "I am happy!", "price to competitors": "Not sure", "price": "low", "pricelimit": { "mostamount": "100", "leastamount": "100" } } },
    { id: 2, postid: "1", json: { "Quality": { "affordable": "3", "does what it claims": "2", "better then others": "2", "easy to use": "3" }, "satisfaction": 3, "suggestions": "better support", "price to competitors": "Not sure", "price": "high", "pricelimit": { "mostamount": "60", "leastamount": "10" } } },
    { id: 3, postid: "2", json: { "member_array_employer": [{}], "partner_array_employer": [{}], "maritalstatus_c": "Married", "member_receives_income_from_employment": "0", "partner_receives_income_from_employment": "0" } },
    { id: 4, postid: "2", json: { "member_array_employer": [{}], "partner_array_employer": [{}], "maritalstatus_c": "Single", "member_receives_income_from_employment": "1", "member_type_of_employment": ["Self-employed"], "member_seasonal_intermittent_or_contract_work": "0" } },
]);
