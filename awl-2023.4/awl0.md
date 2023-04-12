---
title: "Server Actions"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Utilize Urbit as a server backend for automatically handling user sessions, serving materials, etc."
  - "Access `%settings-store` as a supporting system agent."
runes: []
keypoints: []
readings: []
homework: []
mirror: "https://github.com/sigilante/curriculum/blob/master/awl-2023.4/awl0.md"
video: ""
---

#   🖧 `awl0`. Server Actions

One of Urbit's primary use cases is to act as a “personal server”.  To examine this statement, we need to consider what a server does.  Etymologically, a server serves a service.  Generally speaking, it is the locus of a computation and coordination process.  A server program is a system daemon—and since Gall agents are essentially daemons in many respects, Urbit's execution model fulfills this niche nicely.

Some servers are physical or logical devices which talk to other devices as clients.  Internet webpage and application servers typically follow this model.  Other servers are software processes that run on the same hardware or local network as the client process, e.g. mail servers, print servers, and file servers.

![](https://techterms.com/img/lg/client-server_model_1253.png)

The two major operational models for servers are the _request–response_ model and the _publish–subscribe_ (pub-sub) model.  The request–response pattern corresponds to pokes and gifts in Arvo terms, while the pub-sub pattern is supplied by subscriptions and updates.


##  Serving a Web Page

Two of the simplest actions one can take with a basic web server are to simply post a web page to any clients and to respond to interactions with that web page.  Some interactions take place purely in the client session (form entry in the browser before submission), but then are propagated to the server.

### Requests

HTTP requests are like Gall agent pokes:  they are messages to trigger some action on the server.  A method is specified (like `GET`, `PUT`, or `POST`) and the associated service-specific data follow.

It consists of a block of request headers, a block of general headers, and a block of representation headers.  These may by followed by the body.

![](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages/http_request_headers3.png)

### Responses

A [server response to a web page](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages) looks like this:

![](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages/http_response_headers3.png)

The [response code](https://en.wikipedia.org/wiki/HTTP_response_code) is normatively `200 OK` for a successful page access, but `404 Not Found` and other errors and special messages also occur frequently.

The actual mechanics of communicating both kinds of communications are wrapped by `/lib/server` and Eyre.  Generally speaking, your agent will receive HTTP requests in `++on-poke`, and you will commonly include a `++handle-http` arm to deal with `inbound-request:eyre` values.  `/lib/server` has request header parsers and response handlers which make it easy to respond appropriately (e.g. `(send:server ~ [%login-redirect './apps/my-agent'])`).

The [App Workbook](https://developers.urbit.org/guides/additional/app-workbook) includes tutorials on two basic web page servers:  `%feature` and `%flap`.

### `%feature`

[`%feature`](https://developers.urbit.org/guides/additional/app-workbook/feature) is almost the simplest possible Urbit page hosting app.  This uses Quartus' [Schooner](https://github.com/dalten-collective/boat/blob/master/lib/schooner.hoon) library to serve an HTML file at a given binding.  The `POST` request, gated by authentication in the basic version, allows the default page to be changed to a new HTML file.  The `GET` request should (modulo path, status, etc.) return the page head-tagged with `%html` for Eyre to send to the browser.

#### Agent Logic

- `feature-ui` is imported from an HTML file using the `/*` fastar rune.  This simply builds the file using the specified mark.
- `state-0` only contains a `cord` with page content, should you decide to push a new page to the agent (which it will then host instead of `feature-ui`).
- `++on-init` binds the `/apps/feature` endpoint, which will host the web page for the browser.
- `++on-poke` uses a `|^` barket to organize its logic.  This is common in production code where it lies between worth doing inline and worth moving to its own library.
  - The only mark type the agent expects is `%handle-http-request`, a convention arising from Eyre when it passes requests data as a poke to the agent.
  - The source of the request is asserted to be local as a basic security check.  It's also common to see assertion made against `team:sein`, or a point and its moons.
- The `++handle-http` arm in the `|^` barket core takes care of `POST` and `GET` requests.
  - The line `(parse-request-line:server url.request.inbound-request)` functionally serves as a sanity check that the request is well-formed, since the assigned value is not used elsewhere.
  - Recall from our server discussion above that `POST` requests are incoming data.  In this case, the arm unpacks the JSON and associated action, then updates the agent's state with a new HTML page.
  - The `GET` request is a plain vanilla browser display request.  The agent returns the HTML page if the `/apps/feature/public` endpoint is requested, else it requires authentication.  The `%login-redirect` tag automatically tells Eyre how to handle this event.

### `%flap`

[`%flap`](https://developers.urbit.org/guides/additional/app-workbook/flap) is a game app with `%pals`-based leaderboard.  This serves a JavaScript-based game from your Urbit ship, including serving binary data like `WAV` audio files.

The basic concept is to pull an example JS game from GitHub and make minimal changes necessary to incorporate it into Urbit.  While the entire tutorial is worth reading, we highlight a few significant features here.

#### Data Logic

We need to be able to serve a data file with an extension not supported in the regular Urbit binary:  `/audio/wav` for a [WAVE audio file](https://en.wikipedia.org/wiki/WAV_file).  A `WAV` file (and the associated MIME type) provide the musical accompaniment for the game.  The contents of the file is directly served `as-octs:mimes:html` as binary data along the path that JS will expect.

#### Agent Logic

We comment on the "version 2" of `/app/flap.hoon`.  The simple contact manager `%pals` is used as the basis of a leaderboard between friends.

- The necessary files which the agent will serve from the ship are loaded using `/*` fastar.
- `++on-init` binds the Eyre endpoint for communications.
- `++on-load` supports a state upgrade from `%zero` to `%one`.
- `++on-poke` supports direct pokes (`%flap-action`) and HTTP requests.  Most requests are for data, reflected at the various supported endpoint paths.  Everything is head-tagged with its MIME type.  This is used in Schooner to serve the MIME type correctly.  Notice how the Schooner response is curried and then used as a shorthand for responses.

    ```hoon
    =+  send=(cury response:schooner eyre-id)
    [(send [200 ~ [%html flapui]]) this]
    ```

  - JSON wrapping and unwrapping is handled by `++dejs-action` and `++enjs-scores`.
- `++on-agent` handles changes to `%pals`.  If the `%pals` list changes by acquiring a new friend, then a new subscription is sent.  If a friend leaves, then the associated subscription is terminated.


##  Exposing Settings with `%settings-store`

`%settings-store` is a JSON-oriented key-value store which can set persistent ship-wide values in a JSON-compatible format with an API intended for client use.

We can set key-value pairs through pokes, then access the values subsequently through a subscription and the response gifts.

To set values in `%settings-store` for `%mush`, we pass cards like these:

```hoon
::  create an empty bucket for %mush
=/  evt=event:settings  [%put-bucket %mush %lineup *(map key:settings val:settings)]
[%pass / %agent [our.bol %settings-store] %poke %settings-event !>(evt)]
::
::  put an entry in the bucket
=/  evt=event:settings  [%put-entry %mush %lineup `@tas`(desig +.axn) `val:settings`[%s '']]
[%pass / %agent [our.bol %settings-store] %poke %settings-event !>(evt)]
```

To retrieve a value from `%settings-store`, subscribe and receive a gift:

```hoon
::  subscribe to %settings-store
[%pass /lineup %agent [our.bol %settings-store] %watch /bucket/mush/lineup]
::
::  receive a value from %settings-store
++  on-agent
  |=  [wir=wire sig=sign:agent:gall]
  ^-  (quip card _this)
  ?+    wir  (on-agent:def wir sig)
      [%lineup ~]
    ?+    -.sig  (on-agent:def wir sig)
        %fact
      ?+    p.cage.sig  (on-agent:def wir sig)
        ::
        ::  Handle incoming changes from %settings-store
        ::
          %settings-event
        =/  evt  !<(event:settings q.cage.sig)
        ?+    -.evt  (on-agent:def wir sig)
            %put-entry
          `this(lineup (~(put in lineup) key.evt))
          ::
            %del-entry
          `this(lineup (~(del in lineup) key.evt))
          ::
            %del-bucket
          `this(lineup *^lineup)
  ==  ==  ==  ==
```

See [`%global-store`](https://github.com/sigilante/global-store) for an example of a simpler key-value store without the JSON interface.


##  Further Points

- We will discuss handling client redirects with `%band` in `awl5`.
- We will move reverse proxy discussion to a standalone lesson.


##  Exercises

- Read `/lib/server.hoon` to see an example of how [server HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) are handled.  What would it take to implement a new HTTP status code in this library?
- Create a simplified version of `%feature` which only serves a static HTML page—remove all of the unnecessary bits that allow you to upload a new page.  Include a state transition from `%0` to `%1` as a result of this modification.
- Implement a version of [Schooner](https://github.com/dalten-collective/schooner/) which allows a set of MIME types, and corresponding marks.
