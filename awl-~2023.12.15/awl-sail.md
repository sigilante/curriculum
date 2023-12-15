#   ✇ `awl`.  HTML, Sail, and `/lib/rudder`.

##  HTML

A webpage relies on components typically composed in three languages:

1. HTML, HyperText Markup Language, defines the content and semantics of the site.
2. CSS, Cascading Style Sheets, declare the visual styling of the components provided by HTML.
3. JavaScript, used for interactive components.

HTML consists of a series of nodes:  elements have tags, attributes, and contents.

```html
<tag attribute="value">
  Contents
</tag>
```

In Hoon, we can parse HTML from a `cord` using `++de-xml:html`:

```hoon
> =text '<tag attribute="value">Contents</tag>'

> (de-xml:html text)
[ ~
  [ g=[n=%tag a=~[[n=%attribute v="value"]]]
    c=~[[g=[n=%$ a=~[[n=%$ v="Contents"]]] c=~]]
  ]
]
```

The noun syntax for HTML is described in more detail below, but you can see how it designates tags, attributes, and contents.  Without faces you can see a bit more of how it's arranged:

```hoon
[~ [[%tag ~[[%attribute v="value"]]] ~[[~[%$ ~[[%$ "Contents"]]]]]]]
```

`++de-xml` returns a `unit` because it could fail.

This data structure is a great example of the Hoon pattern of using head tags to structurally denote type intent.

`%$` cenbuc is the empty `term`.  (Don't confuse it with `%~` censig, the constant null.)

```hoon
> `@`%$
0
```

`++en-xml:html` processes the other way; here as a round trip (really from `cord` to `tape`):

```hoon
> (en-xml:html (need (de-xml:html text)))
"<tag attribute=\"value\">Contents</tag>"
```

Like JSON, the round trip may not return the identical text to the input, since HTML doesn't care about layout or indentation.  The value should be the same.

~bonbud-macryg
~midden-fabler
~nismut-tamwep
~biszod-winner
Guest
~bonbud-macryg
Guest
~nordus-mocwyl
Guest
In conversation
~sivrul-litsub
Guest
~topdul-fosrus
Guest
polrel-witter
Guest 

##  Sail

> Sail is a domain-specific language for composing HTML (and XML) structures in Hoon.

The point of Sail is to produce HTML as a noun using a Hoon-compatible syntax.  To this end, it doesn't follow HTML syntax but can represent all of the standard elements:  tags, attributes, and contents.

```hoon
;tag(attribute "value"): Contents
```

This produces the same data structure as we saw from `++de-xml`:

```hoon
> ;tag(attribute "value"): Contents
[[%tag [%attribute "value"] ~] [[%$ [%$ "Contents"] ~] ~] ~]
```

So now it's time to talk about the data structures of Sail:

### Types

```hoon
+$  mane  $@(@tas [@tas @tas])                    ::  XML name+space
+$  manx  $~([[%$ ~] ~] [g=marx c=marl])          ::  dynamic XML node
+$  marl  (list manx)                             ::  XML node list
+$  mars  [t=[n=%$ a=[i=[n=%$ v=tape] t=~]] c=~]  ::  XML cdata
+$  mart  (list [n=mane v=tape])                  ::  XML attributes
+$  marx  $~([%$ ~] [n=mane a=mart])              ::  dynamic XML tag
```

These are complicated to recall, but fortunately you don't encounter most of them very often.  Most of the time, your top-level data return will be a `+$manx`, and it will contain a `(list manx)` or `+$marl`.

```hoon
> ;tag(attribute "value"): Contents
[[%tag [%attribute "value"] ~] [[%$ [%$ "Contents"] ~] ~] ~]

> `manx`[[%tag [%attribute "value"] ~] [[%$ [%$ "Contents"] ~] ~] ~]
[ g=[n=%tag a=~[[n=%attribute v="value"]]]
 c=~[[g=[n=%$ a=~[[n=%$ v="Contents"]]] c=~]]
]
```

The bunt of `+$manx` is simply an empty tag:

```hoon
> *manx
[g=[n=%$ a=~] c=~]

> (en-xml:html *manx)
"<></>"
```

What are those other data types for?

- `+$mane` XML [namespace](https://www.w3.org/TR/xml-names/) provides a way of qualifying element/attribute names within scopes.
- `+$mars` XML [CDATA](https://www.w3.org/TR/REC-xml/#dt-chardata) contains character data, data that could be interpreted erroneously as escape blocks for text.  These are representable (since they're part of the standard), but `++de-xml` seems to ignore them.

There are also several marks used to interconvert representations; you will typically just use `%html`/`/mar/html`, which is the mark used when a cage of HTML is returned from an arm.

### Composition

This document shows how to compose a simple Sail document, taken from the interface of `%pals`:

```hoon
;html
  ;head
    ;title:"%pals"
    ;meta(charset "utf-8");
    ;meta(name "viewport", content "width=device-width, initial-scale=1");
    ;style:"{(trip style)}"
  ==
  ;body
    ;h2:"%pals manager"

    Keep track of your friends! Other applications can use this list to
    find ships to talk to, pull content from, etc.
  ==
==
```

Let's look at some Sail syntax:

- Empty tags are closed with a `;` following the tag. 

```hoon
;br;
```

- Filled tags are closed with a line break.  Their content is supplied by a `:`.

```hoon
;h1: A Confederacy of Dunces
```

- Nested tags span multiple lines and are closed with a `==`.

There are few special cases in syntax, including among others:

- Everything inside of Sail is automatically in a `tape`, and any line that isn't otherwise captured by a tag becomes a `p` element.
- “Any text with atom auras or `++arm:syntax` in plain text lines will be wrapped in `<code>` tags.”
- “If we want to write a string with no tag at all, then we can prepend those untagged lines with `;` and then a space:”
- `;img@"url";` → `<img src="some-url" />`

Why use Sail instead of a `cord` of HTML?  Sail allows you to dynamically build components in web pages.  To do this, we need four runes:

- [`;+` miclus](https://docs.urbit.org/language/hoon/guides/sail#-miclus) produces a `+$marl` from a single `+$manx` element.  It's often used to build elements from Hoon logic.
- [`;*` mictar](https://docs.urbit.org/language/hoon/guides/sail#-mictar) produces a `+$marl` from Hoon code yielding a `+$marl`.
- [`;=` mictis](https://docs.urbit.org/language/hoon/guides/sail#-mictis) produces a `+$marl` from a series of `+$manx` elements.
- [`;/` micfas](https://docs.urbit.org/language/hoon/guides/sail#-micfas) produces a `+$manx` from a `tape` (including type interpolation).  It will need a `;+` to produce the `+$marl`.

(Cargo-cult their usage for starters.)

- Take a look at [`/app/pals/webui/index`](https://github.com/Fang-/suite/blob/master/app/pals/webui/index.hoon).  Locate the `++page` arm.  (You don't need to know anything about `/lib/rudder` yet to interpret this arm.)
  - What type does it yield?
  - How does it build the list of `%mutual` pals?  Trace this process.

Sail is slightly quirky.  It would be nice to see some of the special-cased syntax, like for `img`, to be cleaned up.

- [“Sail (HTML)”](https://docs.urbit.org/language/hoon/guides/sail)

### Serving HTML

If you have bound an Eyre endpoint to your agent, you can handle pokes.  You receive a poke at `++handle-http-request` of type `+$inbound-request:eyre`.

```hoon
::  +inbound-request: +http-request and metadata
::
+$  inbound-request
  $:  ::  authenticated: has a valid session cookie
      ::
      authenticated=?
      ::  secure: whether this request was encrypted (https)
      ::
      secure=?
      ::  address: the source address of this request
      ::
      =address
      ::  request: the http-request itself
      ::
      =request:http
  ==
```

The typical pattern is to have an arm like `++handle-http` that you call on the unvased `+$inbound-request`.  This arm checks the REST method (`%'POST'` or `%'GET'`) and returns a server response of some kind.  This is a code and some metadata and data.

Important [server response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) for Urbit as a server include:

- `200 OK` with the page data as a `cage` of `[%html page]`.
- `302 Found` used to redirect for login if unauthenticated.
- `404 Not Found` if no result can make sense for the request.
- `405 Method Not Allowed` if the REST request is ill-formed.

(I would like to see `402 Payment Required` implemented with a native cash system.)

From the Sail perspective, you need to return the `++en-xml:html`ed `+$manx`.

- Compare things like [`%feature`](https://docs.urbit.org/userspace/apps/examples/feature#app-agent-files) and [`%blog`](https://github.com/thecommons-urbit/blog) which only expose peeks and pokes and do no HTML construction in the agent at all, simply returning `404` or `200` with the prepackaged page content.


##  `/lib/rudder`

`/lib/rudder` is part of the `%pals`-verse by ~palfun-foslup.  It describes itself as a “framework for routing and serving simple web frontends.”  To start, you need to import `/lib/rudder` and the webpages:

```
/+  rudder
/~  pages
    (page:rudder [data-from-state] ?(command action))
    /app/my-agent/webui
```

This builds all pages under `/app/my-agent/webui` as entries in a `map`.  Typically the agent state data is the `data-from-state` input to the `+$page:rudder` mold.

Your agent calls `++steer:rudder` in `++on-poke`'s `%handle-http-request` branch, e.g.:

```hoon
%.  [bol !<(order:rudder vase) +.state]
%-  (steer:rudder _+.state ?(trigger decide query))
:^    pages
    (point:rudder /apps/[dap.bol] & ~(key by pages))
  (fours:rudder +.state)
```

This simply returns the right response back from the poke and you don't need to worry about those details.

`/lib/rudder` builds a page with three arms in particular:

- `++build` is called for `GET` requests and produces a rendering of the page.
- `++argue` is called for `POST` requests and produces a command.
- `++final` is called after `POST` requests to handle updating the rendered view.

```hoon
++  page
  |*  [dat=mold cmd=mold]
  $_  ^|
  |_  [bowl:gall order dat]
  ++  build  |~([(list [k=@t v=@t]) (unit [? @t])] *reply)
  ++  argue  |~([header-list:http (unit octs)] *$@(brief cmd))
  ++  final  |~([success=? msg=brief] *reply)
  --
```

It also exposes the `++steer` arm, as mentioned previously.  This is the primary helper and internally handles `GET`/`POST` requests.

- Scan through `++apply` in `/lib/rudder`.
- Look at several examples of `/lib/rudder` in practice from the Examples section below.

One of the difficulties in working with Rudder today is that it requires all of the state variables as an input and output, which is awkward since the page is built at the Ford rune level and you haven't yet defined the state type in the `/app` file.  One workaround is to put the agent state into the `/sur` file so it is available before the `/~` fassig build of `pages`.

If you're interested in contributing to the future of `/lib/rudder`, join the `~polwex/super-rudder` group.

### Resources

- [`/lib/rudder`](https://github.com/Fang-/suite/blob/master/lib/rudder.hoon)
- [`/lib/schooner`](https://github.com/urbit/yard/blob/main/desk/lib/schooner.hoon) (originally Quartus, now in the `%yard` desk)
- [`/lib/mast`](https://github.com/R-JG/mast/) which is an alternative HTML renderer.  Mast is simpler than Rudder but easier to implement (at the cost of some features).

### Examples

- [~littel-wolfur, `%fart`](https://github.com/ryjm/fart) for JS and MP3 direct integration
- [~nordus-mocwyl, `%focus`](https://github.com/brbenji/focus)
- [~lagrev-nocfep, `%emissary`](https://github.com/sigilante/emissary)
