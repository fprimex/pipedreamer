class PipedreamAPI(object):
    "Class generated from Pipedream REST API documentation. See github.com/fprimex/api_gen."

    def __init__(self):
        pass

    def call(self, path, query=None, method='GET', data=None,
             files=None, complete_response=False,
             **kwargs):
        pass

    # Duplicate API endpoint discarded:
    # auto_subscription_create from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-13

    # Duplicate API endpoint discarded:
    # component_create from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint

    # Duplicate API endpoint discarded:
    # component_show from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-2

    # Duplicate API endpoint discarded:
    # components_registry_show from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-3

    # Duplicate API endpoint discarded:
    # orgs_<org_id>_sources_list from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-7

    # Duplicate API endpoint discarded:
    # orgs_<org_id>_subscriptions_list from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-6

    # Duplicate API endpoint discarded:
    # source_delete from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-11

    # Duplicate API endpoint discarded:
    # source_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-4

    # Duplicate API endpoint discarded:
    # source_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#notes-and-examples

    # Duplicate API endpoint discarded:
    # source_events_delete from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-5

    # Duplicate API endpoint discarded:
    # source_update from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-10

    # Duplicate API endpoint discarded:
    # sources__create from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-9

    # Duplicate API endpoint discarded:
    # subscription_create from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-12

    # Duplicate API endpoint discarded:
    # subscriptions_delete from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-14

    # Duplicate API endpoint discarded:
    # users_me from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-19

    # Duplicate API endpoint discarded:
    # users_me_sources_ from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-8

    # Duplicate API endpoint discarded:
    # users_me_subscriptions from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-20

    # Duplicate API endpoint discarded:
    # users_me_webhooks from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-21

    # Duplicate API endpoint discarded:
    # v1_workflow_$errors_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#notes-and-examples-3

    # Duplicate API endpoint discarded:
    # v1_workflow_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#notes-and-examples-2

    # Duplicate API endpoint discarded:
    # webhook_create from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-15

    # Duplicate API endpoint discarded:
    # webhook_delete from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-16

    # Duplicate API endpoint discarded:
    # workflow_$errors_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-18

    # Duplicate API endpoint discarded:
    # workflow_$errors_event_summaries&expand=event from
    # https://pipedream.com/docs/api/rest//pipedream#notes-and-examples-3

    # Duplicate API endpoint discarded:
    # workflow_event_summaries from
    # https://pipedream.com/docs/api/rest//pipedream#endpoint-17

    # Duplicate API endpoint discarded:
    # workflow_event_summaries&expand=event from
    # https://pipedream.com/docs/api/rest//pipedream#notes-and-examples-2

    def auto_subscription_create(self, data, event_name=None, listener_id=None, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-13"
        api_path = "/auto_subscriptions"
        api_query = {}
        if "query" in kwargs.keys():
            api_query.update(kwargs["query"])
            del kwargs["query"]
        if event_name:
            api_query.update({
                "event_name": event_name,
            })
        if listener_id:
            api_query.update({
                "listener_id": listener_id,
            })
        return self.call(api_path, query=api_query, method="POST", data=data, **kwargs)

    def component_create(self, data, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint"
        api_path = "/components"
        return self.call(api_path, method="POST", data=data, **kwargs)

    def component_show(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-2"
        api_path = "/components/{id}"
        api_path = api_path.format(id=id)
        return self.call(api_path, **kwargs)

    def components_registry_show(self, key, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-3"
        api_path = "/components/registry/{key}"
        api_path = api_path.format(key=key)
        return self.call(api_path, **kwargs)

    def orgs_sources_list(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-7"
        api_path = "/orgs/{id}/sources"
        api_path = api_path.format(id=id)
        return self.call(api_path, **kwargs)

    def orgs_subscriptions_list(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-6"
        api_path = "/orgs/{id}/subscriptions"
        api_path = api_path.format(id=id)
        return self.call(api_path, **kwargs)

    def source_delete(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-11"
        api_path = "/sources/{id}"
        api_path = api_path.format(id=id)
        return self.call(api_path, method="DELETE", **kwargs)

    def source_event_summaries(self, id, expand=None, limit=None, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-4"
        api_path = "/sources/{id}/event_summaries"
        api_path = api_path.format(id=id)
        api_query = {}
        if "query" in kwargs.keys():
            api_query.update(kwargs["query"])
            del kwargs["query"]
        if expand:
            api_query.update({
                "expand": expand,
            })
        if limit:
            api_query.update({
                "limit": limit,
            })
        return self.call(api_path, query=api_query, **kwargs)

    def source_events_delete(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-5"
        api_path = "/sources/{id}/events"
        api_path = api_path.format(id=id)
        return self.call(api_path, method="DELETE", **kwargs)

    def source_update(self, id, data, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-10"
        api_path = "/sources/{id}"
        api_path = api_path.format(id=id)
        return self.call(api_path, method="PUT", data=data, **kwargs)

    def sources__create(self, data, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-9"
        api_path = "/sources/"
        return self.call(api_path, method="POST", data=data, **kwargs)

    def subscription_create(self, data, emitter_id=None, event_name=None, listener_id=None, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-12"
        api_path = "/subscriptions"
        api_query = {}
        if "query" in kwargs.keys():
            api_query.update(kwargs["query"])
            del kwargs["query"]
        if emitter_id:
            api_query.update({
                "emitter_id": emitter_id,
            })
        if event_name:
            api_query.update({
                "event_name": event_name,
            })
        if listener_id:
            api_query.update({
                "listener_id": listener_id,
            })
        return self.call(api_path, query=api_query, method="POST", data=data, **kwargs)

    def subscriptions_delete(self, emitter_id=None, event_name=None, listener_id=None, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-14"
        api_path = "/subscriptions"
        api_query = {}
        if "query" in kwargs.keys():
            api_query.update(kwargs["query"])
            del kwargs["query"]
        if emitter_id:
            api_query.update({
                "emitter_id": emitter_id,
            })
        if event_name:
            api_query.update({
                "event_name": event_name,
            })
        if listener_id:
            api_query.update({
                "listener_id": listener_id,
            })
        return self.call(api_path, query=api_query, method="DELETE", **kwargs)

    def users_me(self, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-19"
        api_path = "/users/me"
        return self.call(api_path, **kwargs)

    def users_me_sources_(self, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-8"
        api_path = "/users/me/sources/"
        return self.call(api_path, **kwargs)

    def users_me_subscriptions(self, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-20"
        api_path = "/users/me/subscriptions"
        return self.call(api_path, **kwargs)

    def users_me_webhooks(self, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-21"
        api_path = "/users/me/webhooks"
        return self.call(api_path, **kwargs)

    def webhook_create(self, data, description=None, name=None, url=None, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-15"
        api_path = "/webhooks"
        api_query = {}
        if "query" in kwargs.keys():
            api_query.update(kwargs["query"])
            del kwargs["query"]
        if description:
            api_query.update({
                "description": description,
            })
        if name:
            api_query.update({
                "name": name,
            })
        if url:
            api_query.update({
                "url": url,
            })
        return self.call(api_path, query=api_query, method="POST", data=data, **kwargs)

    def webhook_delete(self, id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-16"
        api_path = "/webhooks/{id}"
        api_path = api_path.format(id=id)
        return self.call(api_path, method="DELETE", **kwargs)

    def workflow_event_summaries(self, workflow_id, errors, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-18"
        api_path = "/workflows/{workflow_id}/{errors}/event_summaries"
        api_path = api_path.format(workflow_id=workflow_id, errors=errors)
        return self.call(api_path, **kwargs)

    def workflow_event_summaries(self, workflow_id, **kwargs):
        "https://pipedream.com/docs/api/rest//pipedream#endpoint-17"
        api_path = "/workflows/{workflow_id}/event_summaries"
        api_path = api_path.format(workflow_id=workflow_id)
        return self.call(api_path, **kwargs)


