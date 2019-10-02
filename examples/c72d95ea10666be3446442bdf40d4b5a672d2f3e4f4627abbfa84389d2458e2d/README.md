## Sample Info

Hash: [c72d95ea10666be3446442bdf40d4b5a672d2f3e4f4627abbfa84389d2458e2d](https://www.virustotal.com/gui/file/c72d95ea10666be3446442bdf40d4b5a672d2f3e4f4627abbfa84389d2458e2d/detection)

### Short Description

A variant of the Mirai botnet malware that contains a Domain Generation Algorithm (DGA). The DGA of this particular sample generates one domain per day, with some exceptions on specific dates. This sample appears to be of the same variant reported by [Netlab](https://blog.netlab.360.com/new-mirai-variant-with-dga/); as we can observe the same hardcoded C2 domain being contacted (__zugzwang.me__) and the same general DGA of one-domain-per-day from the same set of TLDs (online/tech/support), same domain structure, and similarly seeded by year/month/day. 

Unlike previous analysis, however, we are able to emulate many years of execution and record the generated domains, rather than needing to reimplement the DGA. Using this approach, we recorded the domains generated over the 6 year period of 2016-1-1 through 2021-12-31, and discovered _only 428 unique domains_. Additionally, we observed two quirks of the generated domains: 

- There is only a _single_ domain generated from November 1st to December 3rd of every year.
- Only _two_ TLDs are ever used (tech/online), as opposed to the three TLDs discovered by Netlab (tech/online/support)

Upon further reverse engineering, we suspect that the reason for these two behaviors are due to a bug in the original DGA implementation. We believe that _intended_ behavior includes random domains betweeen November 1st and December 3rd, as well as using the third TLD mentioned above (support). 
