---
title: "Front End"
teaching: 60
exercises: 30
nodes: []
objectives:
  - "Produce agents with Urbit-served front ends for the user experience."
runes: []
keypoints: []
readings:
  - "https://developers.urbit.org/guides/quickstart/chat-guide"
  - "https://developers.urbit.org/guides/quickstart/groups-guide"
  - "https://github.com/tadad/blog"
  - "https://github.com/matthew-levan/band"
  - "https://github.com/belisarius222/poast"
homework: []
mirror: []
video: []
---

#   🖵 `awl5`.  Front End.

In this exercise, we will look at apps with some straightforward front-end renderings to the browser client session.

In many ways this hearkens back to `awl0`, wherein we were concerned with treating Urbit as a server.  This time we will examine more of how the front-end is rendered and how client sessions are handled.

##  `%squad`:  Group Management

- https://developers.urbit.org/guides/quickstart/groups-guide
- https://developers.urbit.org/guides/additional/sail

Install from `~pocwet/squad`.

##  `%hut`:  Chat App

- https://developers.urbit.org/guides/quickstart/chat-guide

Install from `~pocwet/hut`.  `%squad` is a prerequisite for `%hut` to run correctly.

##  `%blog`:  Simple Blog Publication

- https://github.com/tadad/blog

Install from `~hanrut-sillet-dachus-tiprel/blog`.

##  `%board`:  Per-User State Management

- https://github.com/hanfel-dovned/Board

Install from `~dister-hanfel-dovned/board`.

##  `%band`:  Redirects and External API

- https://github.com/matthew-levan/band

The `%band` payment processor app uses the Stripe API to process transactions.  It also has a redirect to a success page or a cancellation page.

### Challenge:  Produce forum software with threaded conversation

Using `%hut` as a basis, produce a chat app which can thread conversations.  This means that each comment can have a parent comment, and that there is an affordance in the interface to view one thread by itself without intervening extraneous comments.

##  Further Examples

- `%poast` illustrates solid-state subscriptions and some use of Sail with Rudder.
  - https://github.com/belisarius222/poast
