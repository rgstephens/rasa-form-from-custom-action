
I'm having trouble triggering a form from a custom action.
The intent is `activate_my_form` and when called directly via an intent, works as expected.
When triggering from a custom action it respons 6 to 9 times






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

Using pyenv  and installing requirements. After, python -m spacy download en_core_web_md

rasa train
rasa shell


