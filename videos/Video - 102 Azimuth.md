---
uuid: 102
layout: node
title: "Description of address space structure."
tags:
 - "%azimuth"
prerequisites:
  - "0"
postrequisites:
  - "112"
  - "302"
objectives:
  - "Understand the role of the public-key infrastructure in Urbit."
  - "Describe the high-level architecture of the Urbit ID address space and distinguish types of points."
  - "Interpret and apply the Azimuth point naming scheme."
  - "Identify point features such as activity."
  - "List at least two services/roles provided by a galaxy for the network."
  - "List at least two services provided by a star for its planets."
runes:
  - ""
irregular:
  - ""
key_points: []
assessments: []
comments: ""
content: ""
---

#   Azimuth, The Urbit Address Space

When two parties need to communicate with each other securely, they prefer to use some form of key-based cryptography.  Key-based cryptography allows you to share one key, called a public key, with everyone, while you retain the other key privately.  One encrypts a message using the private key, and another party can only read the message if he or she uses the public key to decrypt the message.  Thus the ability to send an encrypted message decryptable by the public key requires ownership of the private key, and demonstrates one's identity in a fake-proof way.

Urbit ID, or Azimuth, is a public-key infrastructure which provides the basis of identity and identity-based capabilities in Urbit.  An Urbit ID is like a wallet which contains a secret key to boot an Urbit ship that will hold a private key to send signed messages.  Urbit ID serves as a secure, persistent, and futureproof identity for the Urbit network.

An Azimuth address, or _point_, is a 128-bit address.  Since different points bear different rights and duties within the scheme of Urbit, the points are divided into hierarchical bands.

- The first 2⁸ or 256 points are called _galaxies_.  Galaxies serve as the core network infrastructure and governance, similar to ICANN and DNS providers on the Internet as a whole.
- The next points up to 2¹⁶ or 65,536 are called _stars_.  Stars are currently oriented towards software distribution and address space allocation, but eventually will facilitate peer discovery as well.
- The points up to 2³² or about 4 billion are called _planets_.  Planets serve as primary single-user identities.
- Each planet can spawn 2³² _moons_, ultimately intended as subsidiary identities or devices.
- Finally, the remainder of the address space to 2¹²⁸ is reserved for transient identities called _comets_.  Comets are intended for short-term usage or automated bot processes, and don't actually have a separate public key in Azimuth.  Possession of the comet is ownership with no further cryptographic guarantees.

Each point in Azimuth corresponds to a single number from 0 to 2¹²⁸, but as remembering large numbers accurately is difficult, a mnemonic system called `@p`s was introduced.  This assigns one or more syllables to each point deterministically.  The `@p` allows a user to assess network role and easily remember particular individuals using Urbit.

A galaxy `@p` consists of a single syllable, such as `~zod` or `~fes`.

A star `@p` consists of two syllables, such as `~marzod` or `~fipfes`.  Prefix syllables are different from suffix syllables.

A planet `@p` has four syllables, and most Urbit users identify themselves using a planet.

Moons have six to eight syllables depending on their parent, and comets have ten to sixteen syllables.

---

Each Urbit ID point can be associated with a corresponding Urbit OS _ship_.  This is a one-to-one correspondence, and _double-booting_ a ship can lead the network to be in an inconsistent state.

When two ships communicate, each signs the packets with its own private key, and the other ship uses the Azimuth public key infrastructure to locate the appropriate public key and decrypt the packet.

Each ship below a galaxy has a _sponsor_.  One of the roles of a sponsor is to find a path between two ships that wish to communicate but don't yet have a peer-to-peer route.

Sponsors are also responsible for distributing system software updates.

`~zod` acts as the root node for the entire network.  However, Azimuth PKI is itself bootstrapped on top of Ethereum, and any Urbit ship can directly query the status and public key of any other.
