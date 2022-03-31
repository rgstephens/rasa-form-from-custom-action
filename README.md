
I'm having trouble triggering a form from a custom action.

form runs as expected when called from intent:

    Your input ->  hello
    Hey! How are you?
    Your input ->  activate my form
    first I have question
    [My form is asking for a slot]:
    Your input ->  adfadf
    Here is the slot from the form : FAKE ENTITY EXTRACTION
    Your input ->


But running a custom action that should trigger the form:

    Your input ->  hello
    Hey! How are you?
    Your input ->  Custom action intent
    Your input ->

Nothing happens. See debug message at end for output from Rasa.




The way I'm trying to do so is with simulating a user inent using `UserUttered`:

```
slot_events = []
intent = {"intent": {"name": "activate_my_form", "confidence": 1.0}}
utter_event = UserUttered("Activate my form", intent)
slot_events.append(utter_event)
return slot_events
```

I have also tried this in the

```
slot_events.append(SlotSet(key="my_form_trigger", value=True))
```

------------------

I'm using

```
rasa==3.0.9
rasa-sdk==3.0.6
```

In the policy I have
```
policies:
  - name: MemoizationPolicy
  - name: RulePolicy
```


The form is:

```

forms:
  my_form:
    ignored_intents:
    - chitchat
    required_slots:
        - my_slot

```

Slot is:

```
  my_slot:
    type: any
    mappings:
    - type: from_entity
      entity: my_slot
```

For `my_form_trigger`

```
  my_form_trigger:
    type: bool
    influence_conversation: true
    mappings:
    - type: custom
```

The rules looks like so:


```
- rule: Activate My Form
  steps:
  - intent: activate_my_form
  - action: utter_form_start
  - action: my_form
  - active_loop: my_form
  - slot_was_set:
      - my_form_trigger

- rule: Finished with My Form
  condition:
  - active_loop: my_form
  steps:
  # Form is deactivated
  - action: my_form
  - active_loop: null
  - slot_was_set:
    - my_slot: null
  - action: utter_my_form_slots_values
```

## installation

Using pyenv  and installing requirements. After,

    python -m spacy download en_core_web_md

## running

    rasa train
    rasa run actions
    rasa shell -vv

## debug when expected behavior fails


    2022-03-31 12:13:25 DEBUG    rasa.core.lock_store  - Issuing ticket for conversation '93ae2dfd7824465ab395b1d15ffe50bf'.
    2022-03-31 12:13:25 DEBUG    rasa.core.lock_store  - Acquiring lock for conversation '93ae2dfd7824465ab395b1d15ffe50bf'.
    2022-03-31 12:13:25 DEBUG    rasa.core.lock_store  - Acquired lock for conversation '93ae2dfd7824465ab395b1d15ffe50bf'.
    2022-03-31 12:13:25 DEBUG    rasa.core.tracker_store  - Recreating tracker for id '93ae2dfd7824465ab395b1d15ffe50bf'
    2022-03-31 12:13:25 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [<rasa.core.channels.channel.UserMessage object at 0x1afaef460>]}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='f832a7635ad144a0b808a5b94e53e38f', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'nlu_message_converter' running 'NLUMessageConverter.convert_user_message'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'provide_SpacyNLP0' running 'SpacyNLP.provide'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'run_SpacyNLP0' running 'SpacyNLP.process'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'run_SpacyTokenizer1' running 'SpacyTokenizer.process'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'run_SpacyEntityExtractor2' running 'SpacyEntityExtractor.process'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'run_SpacyFeaturizer3' running 'SpacyFeaturizer.process'.
    2022-03-31 12:13:25 DEBUG    rasa.engine.graph  - Node 'run_CountVectorsFeaturizer4' running 'CountVectorsFeaturizer.process'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_DIETClassifier5' running 'DIETClassifier.process'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_EntitySynonymMapper6' running 'EntitySynonymMapper.process'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_ResponseSelector7' running 'ResponseSelector.process'.
    2022-03-31 12:13:26 DEBUG    rasa.nlu.classifiers.diet_classifier  - There is no trained model for 'ResponseSelector': The component is either not trained or didn't receive enough training data.
    2022-03-31 12:13:26 DEBUG    rasa.nlu.selectors.response_selector  - Adding following selector key to message property: default
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_FallbackClassifier8' running 'FallbackClassifier.process'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_LanguageModelFeaturizer9' running 'LanguageModelFeaturizer.process'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_RegexMessageHandler' running 'RegexMessageHandler.process'.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Received user message 'custom action intent' with intent '{'name': 'custom_action_intent', 'confidence': 0.9994083642959595}' and entities '[]'
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 9 events.
    2022-03-31 12:13:26 DEBUG    rasa.core.actions.action  - Validating extracted slots:
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Default action 'action_extract_slots' was executed, resulting in 0 events:
    2022-03-31 12:13:26 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': <rasa.shared.core.trackers.DialogueStateTracker object at 0x1afaef5e0>}, targets: ['select_prediction'] and ExecutionContext(model_id='f832a7635ad144a0b808a5b94e53e38f', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'rule_only_data_provider' running 'RuleOnlyDataProvider.provide'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_MemoizationPolicy0' running 'MemoizationPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.memoization  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: custom_action_intent | previous action name: action_listen
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.memoization  - There is no memorised next action
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_RulePolicy1' running 'RulePolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user text: custom action intent | previous action name: action_listen
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: custom_action_intent | previous action name: action_listen
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_TEDPolicy3' running 'TEDPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ted_policy  - TED predicted 'utter_greet' based on user intent.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_UnexpecTEDIntentPolicy2' running 'UnexpecTEDIntentPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.unexpected_intent_policy  - Querying for intent `custom_action_intent`.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.unexpected_intent_policy  - Query intent index 4 not found in label thresholds - {1: -0.38845077, 5: -0.7065364, 7: -0.026301295, 8: -0.24622284, 9: -0.40931982}. Check for `action_unlikely_intent` prediction will be skipped.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'select_prediction' running 'DefaultPolicyPredictionEnsemble.combine_predictions_from_kwargs'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ensemble  - Predicted next action using RulePolicy.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Predicted next action 'action_default_fallback' with confidence 0.30.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Policy prediction ended with events '[<rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x1afaea4f0>]'.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Action 'action_default_fallback' ended with events '[<rasa.shared.core.events.UserUtteranceReverted object at 0x1af876fd0>]'.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Current slot values:
      my_slot: None
      my_form_trigger: None
      requested_slot: None
      session_started_metadata: None
    2022-03-31 12:13:26 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': <rasa.shared.core.trackers.DialogueStateTracker object at 0x1afaef5e0>}, targets: ['select_prediction'] and ExecutionContext(model_id='f832a7635ad144a0b808a5b94e53e38f', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'rule_only_data_provider' running 'RuleOnlyDataProvider.provide'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_MemoizationPolicy0' running 'MemoizationPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.memoization  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.memoization  - There is a memorised next action 'action_listen'
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_RulePolicy1' running 'RulePolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_TEDPolicy3' running 'TEDPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ted_policy  - TED predicted 'action_listen' based on user intent.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'run_UnexpecTEDIntentPolicy2' running 'UnexpecTEDIntentPolicy.predict_action_probabilities'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.unexpected_intent_policy  - Skipping predictions for UnexpecTEDIntentPolicy as either there is no event of type `UserUttered`, event's intent is new and not in domain or there is an event of type `ActionExecuted` after the last `UserUttered`.
    2022-03-31 12:13:26 DEBUG    rasa.engine.graph  - Node 'select_prediction' running 'DefaultPolicyPredictionEnsemble.combine_predictions_from_kwargs'.
    2022-03-31 12:13:26 DEBUG    rasa.core.policies.ensemble  - Predicted next action using MemoizationPolicy.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Policy prediction ended with events '[]'.
    2022-03-31 12:13:26 DEBUG    rasa.core.processor  - Action 'action_listen' ended with events '[]'.
    2022-03-31 12:13:26 DEBUG    rasa.core.lock_store  - Deleted lock for conversation '93ae2dfd7824465ab395b1d15ffe50bf'.


Activating intent also is an issue


    2022-03-31 12:22:31 DEBUG    rasa.core.lock_store  - Issuing ticket for conversation '61f6d7f4fa2f44e7834b71cf72e8d2b7'.
    2022-03-31 12:22:31 DEBUG    rasa.core.lock_store  - Acquiring lock for conversation '61f6d7f4fa2f44e7834b71cf72e8d2b7'.
    2022-03-31 12:22:31 DEBUG    rasa.core.lock_store  - Acquired lock for conversation '61f6d7f4fa2f44e7834b71cf72e8d2b7'.
    2022-03-31 12:22:31 DEBUG    rasa.core.tracker_store  - Recreating tracker for id '61f6d7f4fa2f44e7834b71cf72e8d2b7'
    2022-03-31 12:22:31 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [<rasa.core.channels.channel.UserMessage object at 0x1b1bcda30>]}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='11ec92063cb6476b839b182307917603', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'nlu_message_converter' running 'NLUMessageConverter.convert_user_message'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'provide_SpacyNLP0' running 'SpacyNLP.provide'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_SpacyNLP0' running 'SpacyNLP.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_SpacyTokenizer1' running 'SpacyTokenizer.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_SpacyEntityExtractor2' running 'SpacyEntityExtractor.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_SpacyFeaturizer3' running 'SpacyFeaturizer.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_CountVectorsFeaturizer4' running 'CountVectorsFeaturizer.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_DIETClassifier5' running 'DIETClassifier.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_EntitySynonymMapper6' running 'EntitySynonymMapper.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_ResponseSelector7' running 'ResponseSelector.process'.
    2022-03-31 12:22:31 DEBUG    rasa.nlu.classifiers.diet_classifier  - There is no trained model for 'ResponseSelector': The component is either not trained or didn't receive enough training data.
    2022-03-31 12:22:31 DEBUG    rasa.nlu.selectors.response_selector  - Adding following selector key to message property: default
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_FallbackClassifier8' running 'FallbackClassifier.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_LanguageModelFeaturizer9' running 'LanguageModelFeaturizer.process'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_RegexMessageHandler' running 'RegexMessageHandler.process'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Received user message 'hello' with intent '{'name': 'greet', 'confidence': 0.9999849796295166}' and entities '[]'
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 20 events.
    2022-03-31 12:22:31 DEBUG    rasa.core.actions.action  - Validating extracted slots:
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Default action 'action_extract_slots' was executed, resulting in 0 events:
    2022-03-31 12:22:31 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': <rasa.shared.core.trackers.DialogueStateTracker object at 0x1b1aed160>}, targets: ['select_prediction'] and ExecutionContext(model_id='11ec92063cb6476b839b182307917603', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'rule_only_data_provider' running 'RuleOnlyDataProvider.provide'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_MemoizationPolicy0' running 'MemoizationPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: greet | previous action name: action_listen
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - There is no memorised next action
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_RulePolicy1' running 'RulePolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user text: hello | previous action name: action_listen
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: greet | previous action name: action_listen
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_TEDPolicy3' running 'TEDPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ted_policy  - TED predicted 'utter_greet' based on user intent.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_UnexpecTEDIntentPolicy2' running 'UnexpecTEDIntentPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Querying for intent `greet`.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Score for intent `greet` is `-1.1194305419921875`, while threshold is `-0.21044859290122986`.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Top 5 intents (in ascending order) that are likely here are: `[('session_start', -0.5387745), ('deny', -0.45278916), ('affirm', -0.3587651), ('mood_great', 0.7020666), ('mood_unhappy', 0.7211871)]`.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Intent `greet-7` unlikely to occur here.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'select_prediction' running 'DefaultPolicyPredictionEnsemble.combine_predictions_from_kwargs'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ensemble  - Predicted next action using UnexpecTEDIntentPolicy.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Predicted next action 'action_unlikely_intent' with confidence 1.00.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Policy prediction ended with events '[<rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x1b1b60460>]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Action 'action_unlikely_intent' ended with events '[]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Current slot values:
      my_slot: None
      my_form_trigger: None
      requested_slot: None
      session_started_metadata: None
    2022-03-31 12:22:31 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': <rasa.shared.core.trackers.DialogueStateTracker object at 0x1b1aed160>}, targets: ['select_prediction'] and ExecutionContext(model_id='11ec92063cb6476b839b182307917603', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'rule_only_data_provider' running 'RuleOnlyDataProvider.provide'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_MemoizationPolicy0' running 'MemoizationPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: greet | previous action name: action_listen
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - There is no memorised next action
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_RulePolicy1' running 'RulePolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    [state 3] user intent: greet | previous action name: action_listen
    [state 4] user intent: greet | previous action name: action_unlikely_intent
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_TEDPolicy3' running 'TEDPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ted_policy  - TED predicted 'utter_greet' based on user intent.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_UnexpecTEDIntentPolicy2' running 'UnexpecTEDIntentPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Skipping predictions for UnexpecTEDIntentPolicy as either there is no event of type `UserUttered`, event's intent is new and not in domain or there is an event of type `ActionExecuted` after the last `UserUttered`.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'select_prediction' running 'DefaultPolicyPredictionEnsemble.combine_predictions_from_kwargs'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ensemble  - Predicted next action using RulePolicy.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Predicted next action 'action_default_fallback' with confidence 0.30.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Policy prediction ended with events '[]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Action 'action_default_fallback' ended with events '[<rasa.shared.core.events.UserUtteranceReverted object at 0x1b1addfa0>]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Current slot values:
      my_slot: None
      my_form_trigger: None
      requested_slot: None
      session_started_metadata: None
    2022-03-31 12:22:31 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': <rasa.shared.core.trackers.DialogueStateTracker object at 0x1b1aed160>}, targets: ['select_prediction'] and ExecutionContext(model_id='11ec92063cb6476b839b182307917603', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'rule_only_data_provider' running 'RuleOnlyDataProvider.provide'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'domain_provider' running 'DomainProvider.provide_inference'.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_MemoizationPolicy0' running 'MemoizationPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.memoization  - There is a memorised next action 'action_listen'
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_RulePolicy1' running 'RulePolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - Current tracker state:
    [state 1] user intent: greet | previous action name: action_listen
    [state 2] user intent: greet | previous action name: utter_greet
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.rule_policy  - There is no applicable rule.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_TEDPolicy3' running 'TEDPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ted_policy  - TED predicted 'action_listen' based on user intent.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'run_UnexpecTEDIntentPolicy2' running 'UnexpecTEDIntentPolicy.predict_action_probabilities'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.unexpected_intent_policy  - Skipping predictions for UnexpecTEDIntentPolicy as either there is no event of type `UserUttered`, event's intent is new and not in domain or there is an event of type `ActionExecuted` after the last `UserUttered`.
    2022-03-31 12:22:31 DEBUG    rasa.engine.graph  - Node 'select_prediction' running 'DefaultPolicyPredictionEnsemble.combine_predictions_from_kwargs'.
    2022-03-31 12:22:31 DEBUG    rasa.core.policies.ensemble  - Predicted next action using MemoizationPolicy.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Policy prediction ended with events '[]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.processor  - Action 'action_listen' ended with events '[]'.
    2022-03-31 12:22:31 DEBUG    rasa.core.lock_store  - Deleted lock for conversation '61f6d7f4fa2f44e7834b71cf72e8d2b7'.