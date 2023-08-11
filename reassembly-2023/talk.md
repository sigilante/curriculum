Since the 2016 public sale, stars have served as the primary public investment vehicle for Urbit.  A star signals that you have a dog in the fight.  Collectively, non-galaxy star investment accounts for a majority of Urbit address space stakeholders, if not of the Urbit address space.  (As of 2023, there were 2,543 unique star holders including galaxies.)  Star bounties and sales have fueled Urbit's development and collective buy-in to the platform, partaking of the web3 NFT craze but not wholly part thereof.

Unfortunately, stars have rather become the middle children of Mars.  The original value proposition, to sell planets, has possibly collapsed due to hosting competition, at least in the short term.  Other value propositions, like transaction validators in sense of the original Uqbar clearpaper, currently seem unlikely to pan out.

It's hard to overstate the disaster that star valuation going to zero would be for Urbit.  Stars have been the primary investment vehicle, the skin in the game.  Rather than shy away from this problem or assume that someone else will fix it, let's engage it directly and see how far we can get.  As a fair warning, the first part of my talk is pretty scary.


##  Ursa Minor (The Bear Case)
GRAPHIC:  URSA MINOR

Stars are nominally intended to serve at least three roles in the Urbit ecosystem:

1. Planet distributors
2. Packet routing
3. Stellar Congress

The model of stars as address-space allocators has served as the primary motivator for star investment in Urbit to date.  Since Urbit doesn't really have the equivalent of stock, you instead own part of the network.  How much that block of address space is or should be worth is a question to address subsequently.

Stars have also been planned as peer discovery and packet routing nodes, a role currently filled by galaxies until the network grows beyond their capacity to accommodate these services.

Finally, stars have been envisioned to provide non-infrastructural governance advisement.  Since Urbit seeks to reduce metapolitical questions to the protocol level and yield the ground of politics to individual communities, it's not clear yet what such advisement would actually look like in practice.  This could include advice and proposals on the nature of Censures or how reputation integrates into the network proper.

Stars are projected to play a key role in keeping the Urbit network running smoothly at scale.  I have heard in the past that the Urbit network protocol Ames should be able to support 10,000 ships daily with current galaxy routing.  Let's suppose this is the right order-of-magnitude; in this case, the total capacity of Urbit with 50% of the galaxies operational would be around 10,000 × 128 = 1.28 MM planets and comets.  Urbit growth is likely several years away from that level of uptake, which means that there is no significant pressure to rely on star routing soon.  In this scenario, stars remain a theoretical need for a while still.

The real problem as of summer 2023 is that there is no clear network incentive for operators to actually run stars.  This is analogous to expecting Bitcoin miners to mine without incentives, and it's untenable.

What does the market value of a star mean?  It's a bet, essentially a prediction market on the extractable value of a star.  If you examine the price data on the Dune dashboard—which is amazing, by the by—you can see that the trend is for stars to have a floor around $2–3,000 lately.  Volume has stayed low and many transfers take place off-chain as private-party transactions so it's hard to get a picture of the entire market.

- [historical chart](https://dune.com/urbitfoundation/urbit)
GRAPHIC:  STAR PRICE CHART

We can carp about the collapse of crypto altcoin value and USD inflation and other supervening factors, but at the end of the day this is the situation we confront.  So as a good starting point for our discussion, we will take what I'll call the default future.  In the absence of any special action taken, what happens to stars and star value?

- Under what circumstances does address space bear value?  The market must not be completely saturated, and hosting pressures must not produce a race to the bottom in terms of onboarding new users.  Neither of these hold, so we can conclude that—effectively—the market value of a planet today is zero dollars.  If stars cannot recoup value from address space, then their role as a planet distributor is largely ceremonial and bears little relation any potential nonzero market value.  Furthermore, it is too late to enforce market scarcity through lockup contracts on either stars or planets.
- Can packet routing lead to value?  There are two scenarios here to recoup value, one in which packet routing is tied to microtransactions—either expedited packet routing for paying sponsees or top-down funding from an entity like the Urbit Foundation.  Neither of these is particularly satisfactory, as microtransaction friction is still a race to the bottom in a commodity market and the UF value proposition becomes circular.  (It may, however, work in the short term to juice the network.)
- Can a seat in the Stellar Congress yield value?  With 2¹⁶ members, it is unlikely that the marginal congressional voice bears enough value to merit attempting to corner the market through purchasing additional stars.

Stars are in an uncomfortable position.  Urbit as a network has a fairly clear value proposition but the more legible investment vehicle is the galaxy which includes governance.  Urbit is a decentralized network that becomes dominated by whales even though there is a way for small-scale investors and the yeomanry to hold address space and capture value.


##  Ursa Major (Star Market)
GRAPHIC:  URSA MAJOR

At the macro level,I have two points to demonstrate today:
1. How does the market for stars reflect any underlying value?
2. How do we express and provide for such value in stars?

The star market is broken right now.  It's hard to reach an entente between buyers and sellers, there's a lot of friction in actual transfers, and the separate markets are fairly decoupled from each other.  There's no escrow.  It's hard to cash out.

There are some decent tools out there to help locate stars for sale, either from private parties or via the wrapped star stack.  These don't solve the fundamental liquidity crisis or the valuation problem however.

Low liquidity is bad for at least three reasons:
1. It's difficult to realize value, and holding a star feels more like holding real estate—it's hard to move and hard to provide a dynamic valuation for.
2. Low liquidity also means that it's hard to play arbitrage games.  In this case, we need some of these to absorb slack in the system.  WSTR should not be strongly decoupled from other star markets, and all of these should be basically in sync with each other.  (Periodically someone pulls their ETH out of the WSTR market and there is no liquidity at all for a while.)
3. Low liquidity contributes to market volatility as single sales and small batches have an outsize effect on the price.

While I like "number go up" as much as anyone, I am arguing not in favor of speculation or investment per se, but that stars inherently have value and that value should be reflected in a fair market price.  This means that we need a working market, which lets the market efficiently make the valuation bet; and a clear statement of stars' prospects for value creation and value capture.

Right now the Urbit Foundation is steward of the `star.market` platform and some associated tools.  This is a reasonable interregnum, but I'll argue for another scenario in a while.

Every star has 65,535 associated planets.  A naïve calculation could tie star value as a multiple of collective planetary value.  Assuming 100% demand, this would peg star value at (2¹⁶-1) × _n_.

| Planet Value | Star Value |
| --- | --- |
| $1 | $65,535 |
| $10 | $655,350 |
| $20 | $1,310,700 |
| $50 | $3,276,750 |

Full saturation of Urbit means 100% utilization of planets and planets bear a stable market price.  In that case, stars possess a value _at least_ equal to the sum value of the planets for which they are responsible.  Less than full saturation means that slack in the market decreases actual value.  That demand will ever saturate supply is a huge assumption.  In an Urbit maximalist scenario, Urbit is running under the hood of the common web much as Linux does today.  The most likely motivator for this would be Urbit actually being easier to use than (say) `nginx` or Apache or what-have-you out of the box.   That's beyond the star value proposition, however, but it's related because it ties to net system demand.

In any case, our conservative operating model for star value must take into account a world in which stars do not “mint out”.  In that world, why operate stars—but even more, why hodl?


##  Stellar Lifecycle
GRAPHIC:  STELLAR LIFECYCLE DIAGRAM

We are going to extend the star metaphor as far as it will go today.  The spectrum of star futures spans from red dwarfs to blue giants.

- Brown dwarf.  Stars are glorified planets.  This is more or less where we are at today, in practical terms.
- Red dwarf.  Stars provide routing, planet distribution, and governance mechanisms.
- Yellow dwarf.  Stars act as centralizers for community coordination and curation.
- Blue giant.  Stars offer a variety of unique and valuable services that are most feasible at their level of access and coordination.

More than that, star behavior in the market is liable to be fueled by a series of subsequent fusion processes.

- **Hydrogen burning.**  Young stars primarily fuse hydrogen.  Early Urbit investment in stars was speculative but undergirt by the backstop promise of planet value.
- **Helium burning.**  As hydrogen grows gradually scarcer in the star, helium becomes the main fuel through the triple-alpha process.  In Urbit terms, if the market value of a planet is zero, then the market value of a star is 65,536×0 = 0.  This has been something of a crisis for star valuation, and has provided strong downward pressure on market prices.  Star values are based on an indeterminate faith, and suitably helium is the first noble gas.
- **Carbon burning.**  As helium starts to exhaust, the star shifts to fusing carbon at a higher temperature.  Functionally, this is what we need right now, and it will require us to be clever and insightful about what stars can and cannot competitively accomplish for Urbit.
- Subsequent fuel processes, including neon, oxygen, and silicon, would correspond to speculative future developments in Urbit.  They are analogically beyond the scope of this talk, but we cannot reach them without burning carbon in the near future.

In other words, to solve our challenge today we need to burn carbon.  Sierra Club hardest hit.


##  Why Hodl
GRAPHIC:  ARECIBO MESSAGE

Let me present a framework for star value.  I don't think this directly communicates to the broader investment world very well.  (I think it's true, and it's a good framework, but it's not terse.)

Most of computing—most of the world—falls into a degenerate para-capitalist state of a tripartite world, like Gaul divided into three parts:  [owners, renters, and maintainers](https://studio.ribbonfarm.com/p/getting-to-gnome-mode?sd=pf), following Venkatesh Rao's analysis.  In particular, conditions of moral hazard obtain for each of the three participant roles:

1. **Owners** tend to be absentee: “Financialization and distance allow you to simply build wear-and-tear into the (very low) cost of capital, and you neglect it the way slumlords do — returns are high enough it’s cheaper to let things run down than to invest in tender, loving, life-extending care of property.”  

2. **Renters** do not own their property and services, so they are incentivized to extract and neglect.  

3. **Maintainers** are relied upon to keep things in good nick, but since they neither own nor use the products in question, they are only invested in surface appearances to fool the owners to whom they are nominally accountable.

The maintainer's dilemma is that, value creation leads to value capture, but everyone fights over value capture more than over value creation.  The star value dilemma is relative of the maintainer's dilemma, where Urbit nominally needs the value creation inherent to stars but does not provide a direct mechanism for value capture.  (This does not mean that I am calling galaxies owners and planets renters.)

We don't want owners to be absentee, so we must resist financialization.  We don't want renters—or users—to be purely neglectful which means that they either have to have some stake or there must be a disincentive to overly harsh value extraction.  (In computing terms, this refers to the essentially disposable relationship we have with almost everything we do online even though we wish it could be more durable.  From the owners' side it also refers to the fact that changes in EULAs can unilaterally deny you of the resources you used, no tenants' rights in play.)  We want the maintainers to be fairly compensated rather than simply squeezed.

The Urbit address space as digital real estate can be used to collapse the owner, the renter/user, and the maintainer back into one person, thereby sidestepping the downsides of financialization.  This is a vision of the yeomanry, however, and centripetal forces will tend to bring large swaths of the network back under the control and value extraction of a plurality of large stakeholders.

Market price acts as a prediction market or a referendum on long-term expected value of an asset.  The market is currently betting that our naïve model is unlikely to pan out.  We'll argue that we have asymmetric information or that we're making a long-tail high-payoff bet on star ownership, but that still requires communicating why stars matter to a functional ecosystem.

- Galaxies derive value from the subsidiary address space they control and from their role in network governance, the Galactic Senate.
- Planets derive value from functioning as peer freeholders.
- Hodling is a bet that stars do arrive at a point of realized value.  How you or I or anyone else is calculating that value is fairly idiosyncratic.  There are enough stars that bringing them under a single entity's control is unlikely in the long run (after dispersion), but not so many that they can stand in for planets.  They are something else besides—so let's explore the ramifications of that middle ground.


##  Constellations
GRAPHIC:  STAR CHART WITH MOTTO

The first motto of my talk is `QVI·PRO·ASTRIS·LOQVITVR`:  who speaks for the stars?

How should stars think of themselves?  Are star owners actually a coherent class or interest group, or are they merely competitors in an ill-defined playing field?  I argue that there are two critical roles stars need to inhabit in order to realize their potential, the first of which being collective organization.

As I mentioned earlier, stars represent table stakes for playing on Mars.  In essence, right now they are a tribal tattoo, much like an MBA.  This isn't bad _per se_ since it's useful for us to have strong affiliation markers, but it's hardly enough.

A collective organization defines a rallying point.  To be clear, I don't mean anything like a union.  Star operators are capitalists in mutual competition.  But the ability to define a neutral forum and common interests and protocols will be critical to securing star value.

I see a role for two distinct organizations motivated by the prior analysis:

1. **The Stellar Congress** is provided for in [Urbit's interim constitution](https://urbit.org/blog/interim-constitution) from 2016.  This group will consist of all active independent stars, defined as stars that are active and .  The purview of the stellar congress is to concern itself with nontechnical network governance.  As I expressed earlier, this group has an identity crisis out of the box:  what does nontechnical governance _mean_?  I think this is underspecified and is a big part of the reason that we have not bothered to actually organize the stellar congress.

2. **The Star Owner's Trade Group**, currently meeting at Provider Standards Organization.  We need some guidance on general wisdom about hodling or operating stars.  We need a suite of standard services, as easy to set up as possible, and we need a coordination locus for hosting providers, star operators, planet merchants, and WSTR hodlers.  

Today we're used to a globally-scoped Urbit network.  The user base hasn't been large enough to start differentiating itself strongly yet.  The stars constitute a large enough playing field that we should see some interesting factional dynamics and game theory play out once they matter.


##  Astrolabe
GRAPHIC:  STAR CHART WITH MOTTO

The second Latin motto of my talk is `OMNES·NAVES·ÆSTVS·NATAT`:  a rising tide floats all ships.  The ownership paradigm of Urbit means that what is good for stars is good for Urbit.  The second critical role for stars to fulfill is that of service provision, hand-in-glove with community structure.  But if every point in Urbit is a fully privileged peer-to-peer node, what does it mean to have star-specific services?  Is this viable?  Is it sustainable?  Or should we just embrace some form of address space agnosticism?

The hierarchy of Urbit is in fact artificial.  There are metapolitical reasons of human intent to have 256 galaxies, but the particulars of galaxies and their number are not entailed by anything in nature.  You and I here likely agree that having a limited galactic senate to contain the spillover of infrastructural decisions is a net good.  So whatever solution we arrive at for stars may be likewise artificial but should be clearly implicated by desired target network dynamics.

Galaxies have a well-defined privileged role, as they hold network governance capabilities.  Stars have been nebulously referred to “internal, but nontechnical, governance”, which is largely unclear:  in a protocol like Urbit, the technical is political.  The composition of an Urbit Constitution has been [slated](https://urbit.org/blog/interim-constitution) for the stars, but we don't even have a stellar congress yet.  So let's table this line for a while.

Star-based value capture will most likely arise from service provision, and so we naturally need to determine which services and how.  One stable locus of attraction is for stars to act as bridges, service providers for services which require more setup and management than a planet owner is likely to want to deal with.  There are a number of Web 2.0 services
enterprise junk

A few months ago, I circulated a document named the [Stella Fixa Memo](https://gist.github.com/sigilante/156329eed993c85cb8e595477c3fa5c2).  In it I argued that “a star operator's value equation includes operating subscription services that are difficult or impossible for planet owners to easily provision for themselves.  … The big value proposition here is bridging Web services that require or strongly incentivize centralization and fixed IP addresses for planet sponsees.”

I documented a number of possible integrations that are “heavy” for planet operators to want to support themselves.  Several of these are hobbled by the enterprise desire to render everything uncodable by the common man, such as single-sign-on support or email service.

I argued as well for stars to provide a layer of financial services handling.  Cryptocurrency transactions can be conducted party-to-party, but there are many reasons to operate financial services from a star, including:
- Payment processing including escrow.
- Lightning channel coordination and funding.
- Coin mixers for anonymization.
- Middleman/brokers for KYCed but otherwise anonymous transactions.

Stars can liaise with VPNs, or provide sponsee-exclusive perks, access, NFTs, events, and so forth.  It's fine to have a gimmick.  They can provide expedited bandwidth or the like much as ISPs do.  They can act as accelerated CDNs for highly in-demand data.

In the long run—if we envision a world where Mars triumphs over the ball of mud, just bridging services is no longer a meaningful process.  Like COBOL, the Web 2.0 services sink into a murky past.  A future-proof solution will need to do better even if the bridge is, well, a bridge.  The things I've listed above are good and we should pursue them, but they are not sufficient in and of themselves.

More accelerated options point to community organization and securement.  In App Workshop, I proposed the `%leek` protocol, a way of actually anonymizing packets on the Urbit network through intermediaries.  A star operating a `%leek` bulb is de facto a darknet, but still a clunky one.  (No worse than Tor, however, operationally.)

“Darknet”, incidentally, is a phrase we've come to associate with illicit activity.  That's a consequence of media and government usage, who clearly have incentives counter to personal privacy and sovereignty, as well as the structure of the word itself.  The thing underlying “darknet” it is appropriate and beautiful.  It's the capability to actually build a community or a platform.  Much like private thought, there must be a suspension of scrutiny to allow free expression, exploration, innovation and creativity.  Without secure enclaves—the snowflake's “safe spaces”, I suppose, in a less weaponized manner—it's impossible to even think clearly.  Harrison Bergeron handicaps for everyone.

Why should stars run a `%rumors` instance for sponsees?  Because anonymous posting is the modern locker room:  it's how you blow off steam, hash out difficult issues, and promote stable group dynamics.  Functional private communities barely exist today because of the global namespacing of the West.  Since one can always gain reputation in the broader world by defecting when crimethink is detected, it's very difficult to speak and think openly.  A high-trust environment is enabled by zero-trust security mechanisms.

Decentralized autonomous organizations are a way that web3 adopters have used to coordinate collective ownership and participation in projects.  I am bullish on a form of DAO that does not yet exist.  Furthermore, I believe that Urbit will afford a better way to organize DAOs than anything on the market today, and in particular stars will play a role in that organization.

There are a couple of interesting ideas put forward by the founder in more recent writings that are applicable here:  optimal autonomous organizations and attested enclaves.  An OAO is a proposal to restructure DAOs—which tend to embody direct democracy—as instead directed autocracies much as joint stock corporations.  An OAO prioritizes executive sovereignty, trustee anonymity, and incentive alignment as a way of stripping out the bureaucratic protocols that gum up and hamstring every institution today.  Stars do not directly provide this, but do provide one way of seeding and coordinating an OAO.  I think it's worth the effort and I think it is viable today to actually run a startup per this protocol on Urbit alone.

Stars can also act in concert to provide what Curtis Yarvin called [“attested enclaves”](https://graymirror.substack.com/p/attested-enclave-networks).  The conceit of a attested enclave is that every node in a network can verify the software that every other node is running.  This does not need to be a network-global verification, merely one which can be enforced across a particular group of ships, such as those subscribed to a star or collection of stars.  There are various guarantees that can accrue to such an attested enclave, not least of which internal transparency and external opacity—the perfect secret garden in which to grow a noncompliant community.

There are a lot of other pieces of such a functional private community web that I'll elide for now.  Suffice it to say that star service provision at the Web 2.0 bridge layer and at the Urbit-native community layer will both be critical to demonstrating star value.

But then why stars, as opposed to anyone else?  Stars are naturally the brokers and guarantors of true decentralization.  They should be more privileged than planets in a social sense because they represent an investment that a planet does not.  This is a moral proposition, so we must translate it into a social proposition and a market proposition.  The only way to do this is for stars to become the gentry class under galaxies as peerage.

What we must avoid, as emphasized in several writings of the founder, is decentralization theater.  “Decentralization theater” results when a project feigns to be decentralized and it is not.  To some extent, that is the current status of Urbit:  a majority of galaxies are controlled by Tlon and the Urbit Foundation.  We expect this to not be a problem in the middle future.  Furthermore, there are (when I checked in July) 2,543 separate addresses holding stars, including about 110 holders of galaxies.  This suggests that star owners are already on a trajectory for a high degree of decentralization.  Clearly DAOs and other protocols could implement schemes such as quadratic voting which are kind of lame but do serve the purpose of watering down whales.

(In fact, we should go one better:  we should structure star value such that it is better expressed through not being centralized, and thus motivate star owners to prefer to disperse and operate stars rather than centralize them.  Stars will become the mainstay of decentralized Urbit.  Ideally the value of operating a star is substantial, but the value delta from operating more than, say, ten stars becomes marginal.)

The value of stars should thus be best manifest by operating them, and should have relatively slight incentives to centralize.  Here is the buried lede of my talk today:  the single biggest value-add for stars to play in the Urbit ecosystem, and the most obvious modality for ongoing value creation and capture, is for stars to act as digital cryptographic signers.  This means defining a meta-protocol within or on top of Azimuth which allows stars or collections of stars to attest transactions and events.  This will allow people to build various kinds of authenticated tools immediately on top of Urbit as Layer Zero.  Urbit provides a natural intersection of personal digital sovereignty and public attestation of such.

Higher-level attested digital signing will support secure messaging, notarized documentation, financial transactions (whether cryptocurrency or fiat), reputation, and autonomous associations.  This capability becomes the backstop of decentralized community.  It moderately centralizes trust by raising pylons to navigate a dark forest by, but it works against full centralization and cooptation by single actors or small cabals.  It doesn't exclude non-star points from implementing their own secure protocols, but it permanently fixes the dynamics of star operations as competitive in a way to guarantee decentrality through incentives.  We should define and develop this concept and build it directly into Azimuth.

At this point, the use of the name “blockchain” may no longer be an apt choice.  This version of [proof-of-identity](https://en.wikipedia.org/wiki/Proof_of_identity_%28blockchain_consensus%29) (PoID) opens up new ways of organizing based on reputation rather than simple consensus, and this should be explored.  Classical proof of identity may as well follow the Bank Secrecy Act for the legacy concepts of “proof of personhood” it employs.  The nice thing about stars is that this doesn't matter in a technological sense.

Alternatively, you should be able to define constellations of stars who can mutually attest to each other with heightened trust, or jointly attest outside the cluster, either as a redundancy mechanism or as a ring signature style anonymization.  We will need mechanisms to guard against the single-source problem, which occurs when one source issues a statement that several other sources repeat, leading to what appears to be multiple confirmations.

Ultimately, what I propose is to build a sufficiently rich base protocol in or on top of Azimuth for a software developer to be able to implement any L1 he prefers on top of Urbit, expecting that the API will be available on every booted point.  We will likely also want to define some sense in which a planet can be sponsored by multiple stars.  All of this can I think be integrated into the Ad Fontes proposal, which is the most ambitious statement of what Urbit-based networking should look like.

Now, the market is not yet mature for a full version of this:  stars are not distributed evenly enough today to prevent 51% attacks or avoid reputation games.  But the elements are there and I think we should see both a signing meta-protocol baked into Urbit and the consequential emergence of multiple L1s directly on top of Urbit.  We could also see token-based software distribution and access:  imagine software distribution, gating, or privilege based on token possession.

Now, there's an ancillary question:  why doesn't anyone just set this up themselves for planets?  Well, does an equivalent operation happen for galaxies?  Is there a circle of planets somewhere feigning itself to be a Planetary Senate and making network governance decisions over their own protocol?  If there is, it's essentially a hard fork and they will end up spinning themselves off out of Urbit.  Rogue planets wandering the trackless spans between stars.  There's an iterated prisoner's dilemma here, but stars hardwired with the capabilities to compete out of the box will have a strong edge.  And ultimately [the stars can go to war](https://urbit.org/blog/the-dao-as-a-lesson-in-decentralized-governance) if necessary, but that's a discussion for another day.


##  Taurus (The Bull Case)
GRAPHIC:  TAURUS

Galaxy–star delamination has proved to be a difficult proposition to navigate, but I do not doubt that we will come to an adequate solution in which we can balance the well-being of the entire equity-based address space.  The challenge of star valuation requires us to create value where now it is only implicit.  By assigning stars a complex role but supported out-of-the-box by Urbit's protocol and software stack, we can thread the needle of building and supporting a truly decentralized Internet.  It's worth hearkening back for a moment to why we emphasize decentralization.  We believe that competitive dynamics will produce better outcomes for everyone.  We believe that collections of people have the right and capacity to cultivate their own culture.  We believe that secure sovereign zones can better establish their own norms for human contentment, with a safeguard in Exit.

That's why Urbit matters.  Urbit is the only game in town to really pursue such a vision.  Solving Urbit's problems does mean moving towards a future that we personally can believe in, a stable patchwork of republics—or other polities.

To summarize my thoughts today:

- There is a need for stars in network traffic, fault isolation, and resource allocation, but there is today scant manifest reason to acquire and operate them.  We have an incentive mismatch.
- A focus on star services can act as a bridge forward and a medium-term revenue and value generation mechanism.
- Star owners need to organize themselves in several forms to promote and nurture these ideas and the ideals of all of Urbit.
- Stars as digital signers become guarantors of Urbit's decentrality and both create and capture value.

GRAPHIC:  CONSCIOUSNESS ENERGY GRID

I have a few calls to action from today's talk as well:

1. PSO/Star Trade Org.  For instance, we need a guide, “So You've Bought Your First Star”.
2. Stellar Congress.  We need to figure out how to constitute this body and the role it will play in more detail.
3. Layer Zero digital signing.  We need to build the L1SDK on Urbit.

Ask not what Mars can do for you, but what you can do for Mars.
