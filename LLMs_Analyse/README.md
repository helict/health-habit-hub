# README

The **LLMs_Analyse/** contains the code related to the evaluation of LLMs on the **habit classification task** and the **habit context classification task** as part of the *Belegarbeit*.
Below is an overview of the file structure:

* **Expose/**
  Contains the exposé written for the *Belegarbeit*.

* **LAMBADA/**
  Contains an attempt to reproduce a data augmentation method called **LAMBADA** ([Anaby-Tavor et al., 2019](https://doi.org/10.48550/arXiv.1911.03118)).
  LAMBADA implements an LLM-based data augmentation pipeline: first, a baseline classifier is trained, then a language model is fine-tuned to generate labeled data, and finally, the generated data is filtered to output a high-quality augmented dataset.

* **LLM-Habit-Classification/**
  Contains the evaluation of LLMs on the **habit classification task**.
  The dataset `HabitDB.xlsx` and the LLM information file `LLMs_info.xlsx` are located in the `scripts/eval` folder.
  The `outputs/` folder contains the results after evaluation (metrics and corresponding cost performance).

* **LLM-Habit-Classification-eng/**
  Contains the evaluation of LLMs on the **habit classification task (English dataset)**.
  The dataset `HabitDB.xlsx` and the LLM information file `LLMs_info.xlsx` are located in the `scripts/eval` folder.
  The `outputs/` folder contains the results after evaluation (metrics and corresponding cost performance).

* **LLM-Habit-context-Classification/**
  Contains the evaluation of LLMs on the **habit context classification task**.
  The dataset `Habit_contexts_DB.xlsx` and the LLM information file `LLMs_info.xlsx` are located in the `scripts/eval` folder.
  The `outputs/` folder contains the results of the evaluation by prompt type (metrics and corresponding cost performance).

* **LLMs_Huggingface/**
  Contains the code used to evaluate LLMs downloaded from Hugging Face on the habit classification and habit context classification tasks.

* **scads-ai-llm-api/**
  Contains the code used to evaluate LLMs from OpenAI and Scads AI on the habit classification and habit context classification tasks.

---

## References

* Anaby-Tavor, A., Carmeli, B., Goldbraich, E., Kantor, A., Kour, G., Shlomov, S., Tepper, N., & Zwerdling, N. (2019). *Not Enough Data? Deep Learning to the Rescue!* arXiv:1911.03118. [https://doi.org/10.48550/arXiv.1911.03118](https://doi.org/10.48550/arXiv.1911.03118)
