"""
Content for the six case study pages. tools/build-case-studies.py renders each
entry into "main pages/zoley-case-study-<key>.v2.html"; build-sections.py then
turns each of those into one self-contained section on the CDN.

Edit copy here, not in the generated pages. Source docs live in the Google Drive
"Case Studies" folder.

Block types used in "story":
  ("p", text)                      paragraph
  ("ul", [items])                  plain bullet list
  ("points", [(title, text)])      numbered cards (e.g. the two structural problems)
  ("parts", [part dicts])          "What we built" cards: label, title, intro, list_title, items, outro
  ("results", [(group, [(value, label, note)])])
  ("diff", [(lead, text)])         "What made the difference" items
"""

# Squarespace URL of the case studies index. The back link on every page points here.
INDEX_URL = "https://www.zoley.io/case-studies"

CASE_STUDIES = [
  # ------------------------------------------------------------------ CRE
  {
    "key": "real-estate",
    "sid": "zly-csd-real-estate",
    "url": "/case-studies/commercial-real-estate",
    "category": "Web Design and Automation",
    "title": "40% more conversions and a faster outreach engine for a commercial real estate brokerage",
    "dek": "Ten to fifteen buyers and investors were raising their hands every day. We rebuilt the website so more of them inquired, then built an outreach engine so every one of them heard back the same day.",
    "anonymized": False,
    "illustration": {"metric": "LEADS CONTACTED THE SAME DAY", "before": ["20%"], "after": ["100%"],
                     "note": "every lead, same day"},
    "snapshot": {
      "client": "No Limit Real Estate, LLC",
      "industry": "Commercial real estate",
      "problem": "The website was leaving interest on the table, and every lead that did arrive meant a string of manual steps. Some waited days for a reply, or never got one.",
      "solution": "A redesigned website and intake process, plus an outreach engine that sends the right property details to every new lead in one click, with safeguards against duplicates.",
      "impact_number": "+40%",
      "impact_text": "more interested conversions from the website, with every lead now contacted the same day.",
      "stats": [("+40%", "interested conversions from the website"),
                ("~8 hrs", "of manual lead handling saved every week"),
                ("100%", "of leads contacted the same day, up from 20%"),
                ("0", "duplicate or incorrect emails sent since launch")],
    },
    "story": [
      ("The situation", [
        ("p", "This brokerage had no shortage of interest. On a typical day, 10 to 15 potential buyers and investors were raising their hands on specific properties. That is a strong pipeline for any commercial real estate team."),
        ("p", "But two gaps were limiting what that interest turned into."),
        ("p", "On the front end, the website and inquiry process were not converting as many visitors as they could. People were browsing listings, but too few of them were taking the next step."),
        ("p", "On the back end, every lead that did come in required a string of manual tasks. Someone had to review it, match it to the right property, find the correct listing PDF, write a personalized email, and keep track of who had already been contacted. At low volume, that is tedious. At real volume, it becomes a bottleneck, and a single missed lead or duplicate email has a real cost."),
      ]),
      ("The real problem", [
        ("p", "In commercial real estate, timing is often the deciding factor. An investor interested in a property is usually looking at several others at the same time. The brokerage that responds first, with the right information, has a meaningful advantage."),
        ("p", "That means two things matter more than anything else: how many interested visitors turn into real leads, and how quickly and accurately each lead gets a response. NLRE had room to improve on both. The website was leaving interest on the table, and the manual follow-up process meant response speed depended on how busy the team was that day. Some leads were not contacted for days, and some were never contacted at all."),
      ]),
      ("Our approach", [
        ("p", "We looked at the full journey, from the moment someone lands on the website to the moment they receive a personalized follow-up, and treated it as one connected system."),
        ("p", "Rather than adding new software, we built everything to run inside tools the brokerage already owned. That kept costs flat, kept the data fully in the brokerage's hands, and meant the system could be shaped around exactly how the team works."),
      ]),
      ("What we built", [
        ("parts", [
          {"label": "Part one", "title": "A new website and intake system", "items": [
            "A redesigned website with a cleaner layout and a clearer path from browsing to inquiring",
            "Property pages structured to make the next step obvious and keep visitors on the site",
            "A structured intake process, so every lead arrives with the information the team needs to respond well",
            "Fewer steps between interest and inquiry, which removes the friction that causes people to leave",
          ]},
          {"label": "Part two", "title": "A systematic outreach engine", "items": [
            "Automated daily lead import that brings in only new leads and skips anyone already contacted",
            "Smart detection that recognizes when the same person is interested in multiple properties",
            "One-click, branded emails that automatically include the correct property PDF, photo, and listing link",
            "Built-in safeguards: a second verification check before every send, automatic duplicate blocking, and locked records, so nothing is ever sent twice by accident",
            "A self-managing property database that keeps active and archived listings organized on its own",
            "Full data ownership, with every lead and every email stored in a system the brokerage controls",
          ]},
        ]),
      ]),
      ("The results", [
        ("results", [
          ("Conversions", [("+40%", "Interested conversions from the website", "")]),
          ("Speed and efficiency", [("~8 hrs", "Manual lead handling saved per week", ""),
                                    ("100%", "Leads contacted the same day", "up from 20%")]),
          ("Accuracy and cost", [("0", "Duplicate or incorrect emails sent since launch", ""),
                                 ("0", "New software subscriptions required", "")]),
        ]),
      ]),
      ("What made the difference", [
        ("diff", [
          ("We fixed both ends of the pipeline.", "More inquiries only help if follow-up keeps pace. By improving the website and the outreach process together, the gains on one side were not lost on the other."),
          ("Speed did not come at the cost of accuracy.", "The safeguards were built on purpose. Sending the wrong property information to a serious investor is a bigger risk than taking an extra second to verify, so the system checks itself before anything goes out."),
          ("Built around the business, not a vendor.", "Because the system lives in tools the brokerage already owns, there is no monthly fee, no data locked in a third-party platform, and no limit on how it can grow."),
        ]),
      ]),
      ("Why it matters for your business", [
        ("p", "Many businesses focus on getting more leads, when the bigger opportunity is often in what happens after someone shows interest. A website that converts better and a follow-up process that runs quickly and consistently can produce more results from the same amount of traffic."),
        ("p", "The right system does not need to be expensive or complicated. It needs to fit how your team actually works, protect you from costly mistakes, and give you back the hours currently spent on repetitive tasks."),
        ("p", "If your team is spending too much time on manual follow-up, or you suspect your website is not converting the interest it gets, we would be glad to take a look."),
      ]),
    ],
    "card": {
      "title": "40% more conversions for a real estate company",
      "tag": "Web design · Automation",
      "headline": "A rebuilt website and a one-click outreach engine for a commercial brokerage. Every lead now hears back the same day.",
      "did": "web design, automation",
      "stat": ("+40%", "interested conversions from the website"),
    },
  },

  # ------------------------------------------------------------------ PT
  {
    "key": "physical-therapy",
    "sid": "zly-csd-physical-therapy",
    "url": "/case-studies/physical-therapy-practice",
    "category": "Strategy and Automation",
    "title": "How a physical therapy practice grew from $300K to $750K a year",
    "dek": "The clinical work was excellent and referrals came in steadily, yet revenue had stalled. We restructured the pricing into clear tiers and built a CRM around how the practice actually runs.",
    "anonymized": True,
    "illustration": {"metric": "ANNUAL REVENUE", "before": ["$300K"], "after": ["$750K"],
                     "note": "same practice, better structure"},
    "snapshot": {
      "client": "A physical therapy practice (name withheld)",
      "industry": "Physical therapy",
      "problem": "Every client paid the same way whatever care they needed, and the operations lived in the owner's head. More demand was turning into more pressure, not more growth.",
      "solution": "A tiered pricing structure matched to each type of client, and a custom CRM that lets the practice deliver every tier consistently.",
      "impact_number": "$750K",
      "impact_text": "in annual revenue, up from roughly $300K, with 20+ admin hours back every week.",
      "stats": [("~$750K", "annual revenue, up from roughly $300K"),
                ("$350", "average revenue per client engagement, up from $125"),
                ("20+ hrs", "of admin time saved every week"),
                ("60%", "of new clients choose a mid or upper tier")],
    },
    "story": [
      ("The situation", [
        ("p", "This practice had everything a growing business should want. The clinical work was excellent, clients were loyal, and referrals came in steadily. From the outside, it looked like a practice on its way up."),
        ("p", "From the inside, it had hit a ceiling. Revenue had been sitting at roughly $300K a year, and the owner was working longer hours just to keep it there. Every new client added a little more weight to a load that was already heavy. More demand was not turning into more growth. It was turning into more pressure."),
      ]),
      ("The real problem", [
        ("p", "When a business stalls, the first instinct is usually to find more customers. In this case, more customers would have made things worse. The practice did not have a demand problem. It had two structural problems that were quietly capping its growth."),
        ("points", [
          ("The pricing did not reflect the value being delivered.", "Every client was offered essentially the same structure, whether they needed an occasional check-in or intensive, ongoing care. That meant the practice was undercharging for its most valuable work. It also meant clients who wanted more support had no clear way to ask for it. The practice was effectively giving away its best services at the same price as its simplest ones."),
          ("The operations lived in the owner's head.", "Client histories, follow-up reminders, scheduling notes, and progress updates were spread across notebooks, text messages, and memory. Follow-ups happened when there was time, not on a schedule. Nothing was wrong exactly, but nothing was built to scale. A practice run this way can only grow as far as one person can personally keep track of."),
        ]),
        ("p", "These two problems were connected. Raising the value of each client relationship only works if the practice can reliably deliver on what it promises. So we treated them as one project."),
      ]),
      ("Our approach", [
        ("p", "We started with how the practice actually creates value, not how it charges for it."),
        ("p", "We looked at the different types of clients the practice served, what each group needed, how much time and attention each one required, and what outcomes they cared about most. Patterns showed up quickly. Some clients wanted light-touch support. Others were deeply invested in their recovery and wanted more structure, more contact, and more accountability. The existing pricing treated both groups the same."),
        ("p", "From there, the plan was simple to state and careful to execute: build a pricing structure that matches each type of client, then build a system that lets the practice deliver every tier consistently without adding to the owner's workload."),
      ]),
      ("What we built", [
        ("parts", [
          {"label": "Part one", "title": "A tiered pricing system",
           "intro": "We restructured the practice's services into clearly defined tiers. Each tier has a specific scope of care, clear deliverables, and a price that matches the value delivered.",
           "list_title": "Why this works", "items": [
            "Clients choose the level of care that fits their goals and budget, instead of being handed a single option",
            "The practice is paid fairly for higher-touch work it was already doing",
            "Pricing is tied to defined outcomes and deliverables, not just time in the room",
            "Clients have a natural path to move up as their needs change",
            "Revenue becomes more predictable, which makes planning and investing easier",
           ],
           "outro": "A well-designed tier structure does something subtle. It changes the conversation from \"how much does this cost?\" to \"which option is right for me?\" That shift alone tends to raise the average value of each client relationship, without any pressure or hard selling."},
          {"label": "Part two", "title": "A custom CRM built around the practice",
           "intro": "Instead of forcing the team into a generic platform full of features they would never use, we built a client management system shaped around how the practice actually runs.",
           "list_title": "Key pieces", "items": [
            "One central record for every client, including history, notes, current tier, and next steps",
            "Automatic follow-up tracking, so no client quietly drifts away between visits",
            "A clear daily and weekly view of who needs attention and why",
            "Visibility into which tiers clients are on and when they may be ready to move up or renew",
            "Less manual admin for the owner and staff",
            "A system the practice fully owns, with no extra subscription to pay for or babysit",
           ]},
        ]),
      ]),
      ("The results", [
        ("results", [
          ("Revenue", [("~$750K", "Annual revenue", "up from roughly $300K"),
                       ("$350", "Average revenue per client engagement", "up from $125"),
                       ("80%", "Share of revenue that is recurring or predictable", "up from 30%")]),
          ("Client behavior", [("60%", "New clients choosing a mid or upper tier", ""),
                               ("25%", "Clients who upgraded tiers after starting care", ""),
                               ("55%", "Clients retained at 3+ months", "up from 20%")]),
          ("Operations", [("20+ hrs", "Admin time saved per week", ""),
                          ("0", "Missed or late follow-ups per week", "down from 15+")]),
        ]),
      ]),
      ("What made the difference", [
        ("p", "The growth did not come from working more hours or raising prices across the board. It came from three things working together."),
        ("diff", [
          ("Pricing that matched value.", "When a price reflects what a client actually receives, both sides feel better about the exchange."),
          ("Structure that made choosing easy.", "Clear tiers gave clients a real decision to make and a clear next step, instead of a single take-it-or-leave-it option."),
          ("A system that made delivery consistent.", "The CRM made sure every client got what their tier promised, every time, without the owner holding it all together personally."),
        ]),
        ("p", "Any one of these would have helped. Together, they changed the direction of the business."),
      ]),
      ("Why it matters for your business", [
        ("p", "Many service businesses hit the same wall this practice did. The work is good, the clients are happy, and yet growth stops. The cause is rarely a lack of demand. More often, pricing has not kept pace with the value being delivered, and the business is running on effort rather than systems."),
        ("p", "Both problems are fixable, and fixing them does not require working harder. Better pricing lets you earn more from the work you already do. A better system lets you handle that work without burning out. That combination is the difference between staying busy and building something that lasts."),
        ("p", "If this sounds familiar, we would be glad to take a look at your business and talk through what is possible."),
      ]),
    ],
    "card": {
      "title": "How we helped a PT get to $750K yearly revenue",
      "tag": "Strategy · Automation",
      "headline": "Tiered pricing and a custom CRM took a stalled physical therapy practice from roughly $300K to $750K a year.",
      "did": "strategy, automation",
      "stat": ("$750K", "annual revenue, up from ~$300K"),
    },
  },

  # ------------------------------------------------------------------ Plastic surgery
  {
    "key": "plastic-surgery",
    "sid": "zly-csd-plastic-surgery",
    "url": "/case-studies/plastic-surgery-email",
    "category": "Automation and Email Infrastructure",
    "title": "Reliable email delivery and instant team alerts for a plastic surgery practice",
    "dek": "One in five of the practice's emails was landing in spam, and new inquiries sat unnoticed for an hour or more. We rebuilt how it sends and how its team hears about new messages.",
    "anonymized": True,
    "illustration": {"metric": "EMAILS LANDING IN SPAM", "before": ["20%+"], "after": ["1%"],
                     "note": "same emails, now they arrive"},
    "snapshot": {
      "client": "A plastic surgery practice (name withheld)",
      "industry": "Plastic surgery",
      "problem": "Patient emails were arriving late or landing in spam, with no error to warn anyone. New inquiries were noticed only when someone happened to check the inbox.",
      "solution": "A dedicated, verified sending platform kept separate from the practice's main address, plus instant alerts that route each new inquiry to the right person.",
      "impact_number": "99.5%",
      "impact_text": "of outbound email now delivered, and new inquiries reach staff in about two minutes.",
      "stats": [("99.5%", "outbound email delivery rate"),
                ("1%", "of emails land in spam, down from 20%+"),
                ("2 min", "for staff to see a new inquiry, down from an hour"),
                ("0", "missed or delayed patient messages since launch")],
    },
    "story": [
      ("The situation", [
        ("p", "In a plastic surgery practice, email carries real weight. Consultation confirmations, pre-op instructions, follow-ups, and replies to new inquiries all depend on messages reaching the right inbox at the right time. Patients considering elective procedures are also comparing practices, and how quickly and professionally a practice communicates is part of that decision."),
        ("p", "This practice's email was inconsistent. Some messages arrived late. Some ended up in spam or promotions folders. And on the inside, the team had no dependable way to know when a new inquiry or form submission came in. Important messages were sometimes noticed hours later, simply because no one was alerted."),
      ]),
      ("The real problem", [
        ("p", "Most people think of email as something that either sends or does not. In reality, every message goes through a series of trust checks before it reaches an inbox. Email providers look at who is sending, whether the sender is properly verified, and whether the sending history looks reliable. If any of those signals are weak, messages get delayed, filtered, or quietly moved to spam."),
        ("p", "Nobody gets an error message when this happens. The practice believes the email was sent, and it was. The patient simply never sees it. That kind of silent failure is the most expensive kind, because nobody knows to fix it."),
        ("p", "The alert problem was related. When new inquiries depend on someone happening to check an inbox, response time depends on luck. For a high-value, high-consideration service, a slow first response can be the difference between a booked consultation and a patient who chose another practice."),
      ]),
      ("Our approach", [
        ("p", "We focused on two outcomes the practice cared about: reliability and convenience."),
        ("p", "Reliability meant making sure every outbound message was properly verified and sent in a way inbox providers trust, while protecting the practice's main email address from any risk."),
        ("p", "Convenience meant the team should never have to think about any of it. Emails should go out on their own, and the right person should be notified the moment something needs attention."),
      ]),
      ("What we built", [
        ("parts", [
          {"label": "Part one", "title": "A reliable outbound email platform", "items": [
            "A dedicated, properly verified sending setup that inbox providers recognize and trust",
            "Separation between automated emails and the practice's main email address, so everyday communication is always protected",
            "Consistent, professional formatting for patient-facing messages",
            "Monitoring that shows whether messages are being delivered, so problems are caught early rather than discovered weeks later",
          ]},
          {"label": "Part two", "title": "Internal alerts that reach the right person", "items": [
            "Instant notifications when a new inquiry, form submission, or important reply comes in",
            "Clear routing, so each type of message goes to the team member who handles it",
            "Alerts that include the key details up front, so staff can act without digging through an inbox",
            "A simple setup that runs in the background, with no new software for the team to learn",
          ]},
        ]),
      ]),
      ("The results", [
        ("results", [
          ("Delivery", [("99.5%", "Outbound email delivery rate", ""),
                        ("1%", "Messages landing in spam or promotions", "down from 20%+"),
                        ("72%", "Open rate on patient communications", "up from 39%")]),
          ("Speed", [("2 min", "For staff to see a new inquiry", "down from 1 hour"),
                     ("1 min", "Average time to first response on new inquiries", "down from 3 hours"),
                     ("100%", "Inquiries responded to the same day", "up from 75%")]),
          ("Business impact", [("80%", "Inquiries that book a consultation", "up from 55%"),
                               ("0", "Missed or delayed patient messages since launch", ""),
                               ("4 hrs", "Staff time saved per week checking and forwarding messages", "")]),
        ]),
      ]),
      ("What made the difference", [
        ("diff", [
          ("We treated email as infrastructure, not an afterthought.", "Delivery is something that has to be set up correctly and protected over time, not assumed."),
          ("We protected what mattered most.", "Keeping automated sending separate from the main practice email meant the most important address was never put at risk."),
          ("We designed for people, not just systems.", "The alerts were built around who needs to know what, and when, so the team spends less time checking and more time responding."),
        ]),
      ]),
      ("Why it matters for your practice", [
        ("p", "Every practice assumes its emails are arriving. Very few actually check. When messages land in spam or new inquiries sit unnoticed, the cost does not show up on any report. It shows up as patients who never booked and follow-ups that never landed."),
        ("p", "A reliable email setup and a smart alert system are not flashy. But they protect every patient conversation your practice has, and they make sure your team hears about new opportunities while they are still warm."),
        ("p", "If you are not certain your emails are reaching patients, or your team is finding new inquiries later than they should, we would be glad to take a look."),
      ]),
    ],
    "card": {
      "title": "Email delivery system for plastic surgery",
      "tag": "Automation · Email",
      "headline": "A verified sending platform and instant team alerts. Spam placement fell from over 20% to 1%, and consultations booked rose to 80%.",
      "did": "automation, email infrastructure",
      "stat": ("99.5%", "outbound email delivery rate"),
    },
  },

  # ------------------------------------------------------------------ DR nonprofit
  {
    "key": "nonprofit-donations",
    "sid": "zly-csd-nonprofit-donations",
    "url": "/case-studies/nonprofit-donation-system",
    "category": "Web Design and Fundraising",
    "title": "How a new website and donation system helped an international nonprofit raise more",
    "dek": "Strong work on the ground, and a website that showed supporters almost none of it. We told the full story, then made giving take only a few steps.",
    "anonymized": True,
    "illustration": {"metric": "AVERAGE GIFT SIZE", "before": ["$10"], "after": ["$50"],
                     "note": "same cause, clearer story"},
    "snapshot": {
      "client": "A nonprofit serving communities in the Caribbean (name withheld)",
      "industry": "International nonprofit",
      "problem": "Supporters live far from the work, and the website told them little about the mission, the people served, or where donations went. Giving took more steps than it should have.",
      "solution": "A new website that answers every question a donor quietly asks, and a donation experience that takes only a few steps and encourages recurring gifts.",
      "impact_number": "+30%",
      "impact_text": "in total donations over the first two months, with the average gift rising from $10 to $50.",
      "stats": [("+30%", "total donations in the first two months after launch"),
                ("$50", "average gift size, up from $10"),
                ("26%", "donation page conversion, up from 8%"),
                ("+20%", "new recurring monthly donors")],
    },
    "story": [
      ("The situation", [
        ("p", "This nonprofit does meaningful, hands-on work in communities across the Dominican Republic. The people it serves see the impact every day."),
        ("p", "The people funding it did not. Most supporters live far from where the work happens, and the organization's website offered little to help them understand it. There was limited information about the mission, few stories about the people served, and no clear explanation of where donations went. Giving itself took more steps than it should have."),
        ("p", "The result was a familiar gap for international nonprofits: strong work on the ground, and a fundraising engine that was not reflecting it."),
      ]),
      ("The real problem", [
        ("p", "Donors give to what they can see and trust. When supporters are thousands of miles away, the website becomes the only window they have into the work. If that window is small, unclear, or out of date, even people who care about the cause hesitate."),
        ("p", "That hesitation usually comes down to a few unspoken questions:"),
        ("ul", ["What exactly does this organization do?",
                "Who does it help, and how?",
                "Where does my money actually go?",
                "Is giving simple and secure?"]),
        ("p", "The old site left most of those questions unanswered. So the problem was not that people did not want to help. It was that the organization was not giving them enough information to feel confident doing so."),
      ]),
      ("Our approach", [
        ("p", "We treated this as a content project as much as a design project."),
        ("p", "A good-looking site with thin information would not have moved donors. What moves donors is clarity: a clear story, specific details, visible impact, and an easy way to act. So we set out to answer every one of those unspoken questions directly on the site, then make giving as simple as possible once someone was ready."),
      ]),
      ("What we built", [
        ("parts", [
          {"label": "Part one", "title": "A website that tells the full story", "items": [
            "A new, modern website designed to build trust from the first visit",
            "A clear explanation of the mission, the communities served, and the specific programs in place",
            "Real stories and photos from the ground, so supporters can see the people and places their gifts reach",
            "Transparent information about how donations are used",
            "Content structured so each page naturally leads to the next step, whether that is learning more or giving",
            "A site the team can keep updated as new projects and stories develop",
          ]},
          {"label": "Part two", "title": "A simple, trustworthy donation system", "items": [
            "A clean donation experience that takes only a few steps from start to finish",
            "Clear calls to give on the pages where supporters are most moved to act",
            "Options for one-time and recurring giving, with a nudge toward recurring donations",
            "Suggested giving amounts tied to real outcomes, so donors understand what their gift makes possible",
            "Automatic thank-you and receipt messages, so every donor feels acknowledged right away",
          ]},
        ]),
      ]),
      ("The results", [
        ("results", [
          ("Fundraising", [("+30%", "Total donations", "vs. the same period before launch"),
                           ("$50", "Average gift size", "up from $10"),
                           ("+20%", "New recurring monthly donors", "")]),
          ("Website performance", [("26%", "Donation page conversion rate", "up from 8%"),
                                   ("4 min", "Average time on site", "up from 30 seconds"),
                                   ("-50%", "Abandoned donations", "")]),
        ]),
      ]),
      ("What made the difference", [
        ("diff", [
          ("Information built confidence.", "The biggest lift came from simply telling supporters what they needed to know. Specific details about programs and impact replaced vague language, and donors responded."),
          ("The story came before the ask.", "Visitors met the people and the work first, and were asked to give once they understood why it mattered."),
          ("Giving became effortless.", "Once someone decided to give, nothing stood in the way. Fewer steps meant fewer people changing their minds halfway through."),
        ]),
      ]),
      ("Why it matters for your organization", [
        ("p", "Many nonprofits assume they need more donors. Often, they already have people who care and are willing to give. What those people need is a clearer picture of the work and a simpler way to support it."),
        ("p", "Donations follow clarity. When supporters can see the mission, understand the impact, and give in a few clicks, more of them do, and they tend to give more often. The work on the ground did not change for this organization. What changed is that the people who wanted to help finally had everything they needed to say yes."),
        ("p", "If your organization is doing great work that supporters are not fully seeing, we would be glad to talk through how to change that."),
      ]),
    ],
    "card": {
      "title": "A donation system for a nonprofit",
      "tag": "Web design · Fundraising",
      "headline": "A website that tells the full story and a few-step donation flow. Donations rose 30%, and the average gift went from $10 to $50.",
      "did": "web design, fundraising",
      "stat": ("+30%", "total donations, first two months"),
    },
  },

  # ------------------------------------------------------------------ Tree nonprofit
  {
    "key": "tree-project",
    "sid": "zly-csd-tree-project",
    "url": "/case-studies/west-hartford-tree-project",
    "category": "Web Design and Automation",
    "title": "A website and intake system that helped a local nonprofit look as good as its mission",
    "dek": "The organization plants trees that improve neighborhoods for decades. Its website looked dated and hid the next step. We rebuilt both the site and the way requests reach the team.",
    "anonymized": False,
    "illustration": {"metric": "VISITORS WHO TAKE ACTION", "before": ["15%"], "after": ["35%"],
                     "note": "same mission, clearer next step"},
    "snapshot": {
      "client": "The West Hartford Tree Project",
      "industry": "Community nonprofit",
      "problem": "A dated website with no clear way to request a tree, volunteer, or give, and requests arriving by email, phone, and message, each missing different details.",
      "solution": "A credible, mobile-friendly website with three obvious paths, and a structured intake system that delivers every request complete and in one place.",
      "impact_number": "1,500",
      "impact_text": "tree requests in the first month, and more than twice the share of visitors taking action.",
      "stats": [("1,500", "tree requests in the first month"),
                ("35%", "of visitors take an action, up from 15%"),
                ("+20%", "volunteer sign-ups"),
                ("-60%", "time spent sorting and following up on requests")],
    },
    "story": [
      ("The situation", [
        ("p", "This organization does something simple and lasting. It puts trees into the ground in its own community, one yard, street, and park at a time. The work is visible, it is local, and it improves neighborhoods for decades."),
        ("p", "Its website told a different story. The design was limited and dated, the mission was hard to find, and it was not clear how someone could request a tree, volunteer, or support the work. Requests came in through a mix of emails, phone calls, and messages, each with different information, which meant the small team spent a lot of time chasing details before any planting could begin."),
      ]),
      ("The real problem", [
        ("p", "For most businesses, a website is a sales tool. For a nonprofit, it is a trust tool."),
        ("p", "Donors, volunteers, and neighbors all ask the same quiet question before they get involved: is this organization legitimate, organized, and worth my time or money? A nonprofit rarely gets to answer that question in person. The website answers it first, often in a matter of seconds."),
        ("p", "A dated site with an unclear next step does not just look unpolished. It suggests, fairly or not, that the organization behind it may be disorganized too. That perception costs volunteers, donations, and community goodwill that the organization has earned through its actual work."),
        ("p", "The intake side had the same problem from the inside. Without a consistent way to collect requests, every new request created extra work, and the team's time went to paperwork instead of planting."),
      ]),
      ("Our approach", [
        ("p", "We designed around two audiences at once."),
        ("p", "For the public, the goal was trust and clarity. Someone landing on the site should understand the mission within seconds, see real evidence of the work, and know exactly what to do next."),
        ("p", "For the team, the goal was simplicity. Every request should arrive complete, organized, and ready to act on, without anyone having to piece it together by hand."),
        ("p", "We also kept one practical constraint front and center. Nonprofit teams are small and often volunteer-run. Anything we built had to be easy to maintain without technical help."),
      ]),
      ("What we built", [
        ("parts", [
          {"label": "Part one", "title": "A website that earns trust", "items": [
            "A clean, modern design that looks credible from the first scroll",
            "A clear mission story told in plain language, supported by real photos of the work",
            "Three obvious paths for the three things visitors want to do: request a tree, volunteer, or support the work",
            "Impact highlights that show what the organization has already accomplished",
            "A layout that works well on phones, where most local visitors first find the site",
            "Pages the team can update on their own as new projects and stories come in",
          ]},
          {"label": "Part two", "title": "A simple, reliable intake system", "items": [
            "A structured request form that collects the same key information every time",
            "All requests organized in one place, so the team can see what is new, pending, and complete",
            "Automatic confirmations, so every person who submits a request knows it was received",
            "Internal notifications, so the right team member sees new requests right away",
            "A clear record of every request, which also makes reporting to donors and partners easier",
          ]},
        ]),
      ]),
      ("The results", [
        ("results", [
          ("Community engagement", [("1,500", "Tree requests received", "in the first month"),
                                    ("+20%", "Volunteer sign-ups", "")]),
          ("Website performance", [("35%", "Visitors who took an action (request, volunteer, or donate)", "up from 15%")]),
          ("Operations", [("-60%", "Time spent sorting and following up on requests", ""),
                          ("< 1 day", "Average time from request to response", "down from up to a week")]),
        ]),
      ]),
      ("What made the difference", [
        ("diff", [
          ("The mission came first.", "Instead of leading with the organization, the site leads with the impact: trees planted, streets changed, neighbors involved. That is what people care about."),
          ("Every visitor had a clear next step.", "Visitors did not have to hunt for how to help. The paths were obvious, which removed hesitation."),
          ("The back office got as much attention as the front.", "A beautiful site that funnels requests into a messy inbox only moves the problem. The intake system made sure more interest turned into less work, not more."),
        ]),
      ]),
      ("Why it matters for your organization", [
        ("p", "Nonprofits often put every dollar and every hour into the mission, which is exactly as it should be. But the website and the systems behind it are part of the mission too. They are how new supporters find you, decide to trust you, and choose to get involved."),
        ("p", "A polished website tells the community that your organization is serious and well run. A simple intake system gives your team back the hours it spends on paperwork. Together, they help a small team do more of the work that matters."),
        ("p", "If your organization's online presence does not reflect the quality of your work, we would be glad to talk about what that could look like."),
      ]),
    ],
    "card": {
      "title": "A website and intake system for a tree nonprofit",
      "tag": "Web design · Automation",
      "headline": "A credible new website with three clear paths and a structured intake system. 1,500 tree requests arrived in the first month.",
      "did": "web design, automation",
      "stat": ("1,500", "tree requests in the first month"),
    },
  },

  # ------------------------------------------------------------------ DMSS
  {
    "key": "dental-staffing",
    "sid": "zly-csd-dental-staffing",
    "url": "/case-studies/dental-staffing-intake",
    "category": "Automation",
    "title": "Automated intake and a lightweight CRM for a dental staffing company",
    "dek": "Shift requests arrived as texts to one staff member's personal phone. We turned them into a pipeline that sorts every request by urgency and logs it where the whole team can see it.",
    "anonymized": False,
    "illustration": {"metric": "WHERE SHIFT REQUESTS LIVE", "before": ["One", "personal phone"],
                     "after": ["A shared", "tracker"], "note": "every request in one place"},
    "snapshot": {
      "client": "Dental Medical Support Systems (DMSS)",
      "industry": "Dental staffing",
      "problem": "Shift requests came in as texts to a personal phone and were read, sorted by urgency, and tracked by hand. Nothing was centralized or searchable.",
      "solution": "A dedicated business number feeding an automated pipeline that reads each request, classifies its urgency, and logs it to a shared tracker.",
      "impact_number": "",
      "impact_text": "Every shift request now lands in one searchable place, sorted by urgency, whether or not one specific person is available.",
      "stats": [],
    },
    "story": [
      ("The situation", [
        ("p", "Dental Medical Support Systems (DMSS) runs on shift requests coming in constantly from dental offices that need coverage. Before this project, those requests came in as texts to a staff member's personal phone, then had to be manually read, sorted by urgency, and tracked by hand."),
        ("p", "Nothing was centralized and nothing was searchable. The person handling it had no system, just a phone, a notepad, and memory."),
      ]),
      ("What we built", [
        ("p", "We built a pipeline that takes shift requests from a dedicated business phone number, routes them automatically through email, and uses a script to read each message, work out how urgent it is, and log it into a shared tracking sheet that acts as a lightweight CRM. No more digging through texts. No more guessing which request came in first or which one is time-sensitive."),
        ("parts", [
          {"label": "Key pieces", "title": "From a text thread to a real pipeline", "items": [
            "A dedicated business number replacing a personal phone for shift requests",
            "Automatic routing, so incoming requests flow into a structured pipeline instead of a text thread",
            "Urgency classification, so the most time-sensitive requests surface first",
            "A centralized tracking sheet the whole team can see and search, instead of one person's inbox",
            "Built as a foundation that can plug into their existing staffing software later, rather than a one-off tool",
          ]},
        ]),
      ]),
      ("The result", [
        ("ul", ["Every shift request is captured and logged automatically, with no manual sorting",
                "The most urgent requests surface first, instead of wherever they fell in a text thread",
                "The whole team can see and search every request, not just the person holding the phone"]),
      ]),
      ("Why it matters", [
        ("p", "This was not about adding software for its own sake. It was about taking a process that lived in one person's phone and turning it into something the business actually owns, something that keeps working whether or not one specific person is available. That is the difference between a workaround and a real system."),
      ]),
    ],
    "card": {
      "title": "Automated shift intake for a dental staffing company",
      "tag": "Automation",
      "headline": "Shift requests used to arrive as texts to one personal phone. Now every one is sorted by urgency and logged where the whole team can see it.",
      "did": "automation",
      "stat": ("1 place", "for every shift request, sorted by urgency"),
    },
  },
]
