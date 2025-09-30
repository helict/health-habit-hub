# Habit classifier based on LLM (determine whether it is a habit and extract the context information of the habit)

This project consists of three main parts:
- The core component is the [API-service](API-service): it can call the external LLM service to determine whether a sentence describes a habit and classify the context of the habit in the sentence. It also calls Redis to reduce the number of LLM calls and thus reduce costs.
- [HHH-service](HHH-service) acts as an intermediary service between users and [API-service](API-service): it can call the services of [API-service](API-service), perform operations, and store the results returned by [API-service](API-service) in the database.
- [hhh-frontend](hhh-frontend): This is the front-end I built with Vue. Users can enter their own sentences, select a language, and get a result.


## Flowchart Diagram.
The following [Flowchart Diagram](flowchartdiagram.png) shows the logic of the entire project

```mermaid
flowchart LR
    A["Unstructured text (multilingual)"]
    B["Component K1: Habit recognition"]
    C{"Text identified as habit?"}
    D["Component K2: Context classification"]
    E["Text as non-habitual"]
    F["Storage in database"]

    A --> B
    B --> C
    C -- "Yes" --> D
    C -- "No" --> E
    D --> F
    E --> F
```

## SequenceDiagram.
The following [Sequence Diagram](sequencediagram.png) shows the logic of the entire project in more detail

```mermaid
sequenceDiagram
    autonumber
    actor Donator as Donator (User)
    participant HHH as HHH Orchestrator
    participant API as API (OpenAPI/Swagger)
    participant LLM as Calling external services (LLMs, Redis)
    participant DB as Storage (MongoDB)

    Donator->>HHH: send(sentence, language)
    HHH->>API: classifyHabit(uuid, sentence, language)
    API->>API: generatePrompt()
    API->>LLM: classifyHabit(prompt,sentence,provider,model,temperature...)
    LLM-->>API: uuid,sentence,language,habit_class (0/1), confidence
    API->>LLM: cache(uuid,sentence,language,habit_class (0/1), confidence)
    API-->>HHH: uuid,sentence,language,habit_class (0/1), confidence

    alt habit_class == 0 (not a habit)
        HHH->>DB: store_habit_data(uuid,sentence,language,habit_class (0/1), confidence)
        HHH-->>Donator: msg("This sentence does not describe a habit, please try again.")
    else habit_class == 1 (is a habit)
        HHH->>DB: store_habit_data(uuid,sentence,language,habit_class (0/1), confidence)
        HHH->>API: classifyContext(uuid,sentence,language)
        API->>API: generatePrompt()
        API->>LLM: classifyContext(prompt,sentence,provider,model)
        LLM-->>API: Output {uuid, sentence,language, [Context...] }
        API->>LLM: cache(uuid, sentence,language, [Context...])
        API-->>HHH: Output { uuid, sentence,language, [Context...] }
        HHH->>DB: store_context_data( uuid, sentence,language, [Context...] )
        HHH-->>Donator: msg("stored successfully！")
    end
```

## Running with Docker
This is mainly for the startup of Docker of the core component [API-service](API-service)
To run the server, go to the [API-service](API-service) directory and do the following:

The first step is to find [example.env](API-service/src/openapi_server/example.env), change its name to .env, and then enter your own __REPLACE_WITH_YOUR_OPENAI_API_KEY__ and __REPLACE_WITH_YOUR_SCADS_API_KEY__, you can also choose the model you want to use.


```bash
docker compose up --build
```

and open your browser at `http://localhost:8080/docs/` to see the docs.


