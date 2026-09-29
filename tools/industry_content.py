"""
Content for the industry pages. tools/build-industry-pages.py renders each entry
into "main pages/zoley-industry-<key>.v2.html"; build-sections.py then publishes
each as one section (key ind-<key>). Edit copy here, not in the generated pages.

Every external figure must have its source logged in Zoley/V2-NOTES.md, section 2.
"""

QUICKSTART = "https://www.zoley.io/find-your-next-best-business-move"
CALENDLY = "https://calendly.com/zoley/zoley-discovery-call"

SERVICE_URLS = {
    "Automation": "https://www.zoley.io/automation",
    "AI": "https://www.zoley.io/artificial-intelligence",
    "Web": "https://www.zoley.io/web-dev",
    "Strategy": "https://www.zoley.io/strategic-consulting",
    "Advertising": "https://www.zoley.io/digital-advertising",
}

# How we work: the homepage's four steps, shared by every industry page.
STEPS = [
    ("Diagnose", "We audit how patients, work, and money actually move through your practice, and where they stall."),
    ("Design", "We rank the fixes by return on effort and scope the first one precisely: deliverables and timeline, in writing."),
    ("Build & connect", "We build inside the tools you already run, document everything, and hand over ownership. No proprietary lock-in."),
    ("Measure", "Every build ships with tracking. We review the numbers with you and adjust, so the result holds up after launch."),
]

INDUSTRIES = [
  # ------------------------------------------------------------------ Dental
  {
    "key": "dental",
    "sid": "zly-ind-dental",
    "url": "/dental-practices",
    "tag": "for dental practices",
    "title": "A front desk that keeps up with your chairs.",
    "sub": "New-patient calls, reminders, recall, and the paperwork between visits. We build the systems that keep a dental practice's schedule full without adding to the front desk's day.",
    "board": {
        "cards": [("New patient", "calls after hours"), ("Instant reply", "text and email"),
                  ("Booked", "reminders sent"), ("Recall", "due in six months")],
        "note": "nothing waits on the front desk",
    },
    "stat": ("~3 in 10", "calls to dental offices go unanswered during business hours, and most new patients who reach voicemail call the next practice instead of leaving a message."),
    "problems_title": "Where dental practices lose patients without noticing.",
    "problems_intro": "None of these show up on a schedule or a P&L. They show up as open chairs and new patients who booked somewhere else.",
    "problems": [
        ("The phone rings while everyone's busy.", "Calls land during check-in, check-out, and lunch. The new patient doesn't leave a message; they try the next office on the list."),
        ("Recall depends on someone running a list.", "Hygiene recall works when a person has time to chase it. When the front desk is stretched, it's the first thing to slip, and the schedule thins out months later."),
        ("No-shows leave chairs empty.", "A reminder that goes out late, or not at all, turns into an empty hour for the hygienist and a gap nobody had time to fill."),
        ("The same details get typed three times.", "Forms, the practice software, the billing system, a spreadsheet. Every re-entry is time off the patient in front of you and a chance for an error."),
    ],
    "builds_title": "What we build for dental practices.",
    "builds_intro": "Each of these is scoped around your practice and built inside the tools you already run. Most practices start with one or two.",
    "builds": [
        ("Automation", "New-patient follow-up", "Every call, form, or text from a new patient gets a reply within minutes, with a link to book, and is logged so nobody has to remember to call back."),
        ("Automation", "Reminders & confirmations", "Confirmations, reminders, and easy rescheduling that go out on time, every time, so fewer appointments turn into empty chairs."),
        ("Automation", "Recall & reactivation", "Patients due for hygiene, or who haven't been in for a while, are contacted on a schedule until they book or opt out."),
        ("Automation", "New-patient welcome guide", "What to expect, what to bring, and how the first visit works, sent automatically after booking. It eases the new-office nerves."),
        ("AI", "Front-desk assistant", "Answers the questions the front desk hears all day (hours, insurance, directions, what a first visit involves) on your site or by text, and hands off to a person when it should."),
        ("Web", "A website built for new patients", "Fast on a phone, clear about what you offer and who you see, and one obvious way to book. Set up to be found when someone nearby searches for a dentist."),
    ],
    "proof": {
        "kind": "case",
        "tag": "from our work",
        "title": "Dental support, rebuilt around one inbox instead of one phone.",
        "text": "A dental staffing company ran on shift requests texted to a staff member's personal phone. We moved them to a dedicated business number and built a pipeline that reads each request, sorts it by urgency, and logs it where the whole team can see it.",
        "points": ["Every request captured and logged automatically", "The most urgent requests surface first", "The whole team can see and search every request"],
        "link": ("/case-studies/dental-staffing-intake", "Read the case study"),
    },
    "quotes": [
        ("Our patients are loving the welcome guide that Zoley put together for us. It goes out automatically and helps give them a clear idea of what to expect when they come into our office and eases the \"new office\" nerves.", "Jessica E.", "Dental Office Manager"),
        ("We were missing so many leads per week until Zoley built us a custom intake system. Now, nothing gets missed, and my team isn't stuck doing the same busywork every day.", "Shirley J.", "Dental Medical Support Services, LLC"),
    ],
    "faq": [
        ("Will this work with our practice management software?", "We build around the systems you already run. The audit starts by confirming what your software can connect to, and we design within that rather than asking you to switch."),
        ("What about patient privacy?", "Patient health information stays in the systems your practice already uses for it. Anything we build that touches patient data is scoped with you before we start, including which tools are allowed to hold it."),
        ("Does this replace our front desk?", "No. It takes the repetitive work off them (the callbacks, the reminders, the re-typing) so they can spend their time on the patients in front of them."),
        ("How long until something is running?", "Most first builds are live within three to five weeks of the audit, and they run in parallel with your current process before we switch over."),
    ],
    "cta_title": "Let's fill the schedule without adding to the front desk.",
    "cta_text": "Tell us how your practice runs today. We'll come back with a written plan: what we'd build first, why, and what it should return.",
  },

  # ------------------------------------------------------------------ Plastic surgery
  {
    "key": "plastic-surgery",
    "sid": "zly-ind-plastic-surgery",
    "url": "/plastic-surgery-practices",
    "tag": "for plastic surgery practices",
    "title": "Every consultation inquiry answered while the patient is still deciding.",
    "sub": "Patients considering elective surgery research several practices at once. How fast and how well you respond is part of how they choose. We build the systems that make sure every inquiry reaches the right person, and every patient email reaches the inbox.",
    "board": {
        "cards": [("Inquiry", "10:42 pm, Saturday"), ("Coordinator", "alerted in minutes"),
                  ("Consult booked", "prep guide sent"), ("Follow-up", "until they decide")],
        "note": "every inquiry, answered warm",
    },
    "stat": ("21×", "more likely to qualify a lead when you respond within five minutes rather than thirty. For a high-consideration procedure, the first practice to answer well has the advantage."),
    "problems_title": "Where consultations slip away.",
    "problems_intro": "Aesthetic patients are comparing practices before they ever walk in. These are the gaps that cost a booked consultation, usually without anyone knowing it happened.",
    "problems": [
        ("Inquiries wait for someone to check.", "A form comes in on a Saturday night and is seen on Monday. By then the patient has heard back from two other practices."),
        ("Emails quietly land in spam.", "Confirmations, pre-op instructions, and replies go out and never arrive. Nobody gets an error message, so nobody knows to fix it."),
        ("Coordinators answer the same questions all day.", "Cost ranges, recovery time, financing, what a consultation involves. Important to answer well, and a large share of the day."),
        ("Interested patients go quiet.", "Elective decisions take time. Without a considered follow-up, a patient who was ready in three months books wherever stayed in touch."),
    ],
    "builds_title": "What we build for plastic surgery practices.",
    "builds_intro": "Scoped around how your practice converts an inquiry into a consultation, and built into the tools your team already uses.",
    "builds": [
        ("Automation", "Instant inquiry alerts & routing", "New inquiries, form submissions, and important replies reach the right coordinator in minutes, with the key details up front."),
        ("Automation", "Reliable email delivery", "A properly verified sending setup, kept separate from your main address, so confirmations and instructions reach the inbox instead of spam."),
        ("Automation", "Consultation nurture", "A considered sequence for patients who aren't ready yet: what to expect, recovery, financing, and an easy way back when they are."),
        ("AI", "Patient-question assistant", "Answers the common questions on your site or by text in your practice's voice, and hands anything that needs judgment to a coordinator."),
        ("Web", "Consultation-focused website", "Procedure pages that answer what patients actually ask, and a clear, polished path to requesting a consultation on a phone."),
        ("Advertising", "Tracked campaigns", "Search and social campaigns with tracking from day one, so you can see which ads produce consultations, not just clicks."),
    ],
    "proof": {
        "kind": "case",
        "tag": "from our work",
        "title": "A plastic surgery practice whose emails weren't arriving.",
        "text": "Patient emails were landing in spam with no warning, and new inquiries were noticed only when someone checked the inbox. We rebuilt how the practice sends email and how its team hears about new messages.",
        "numbers": [("1%", "of emails in spam, down from 20%+"), ("2 min", "for staff to see a new inquiry, down from an hour"), ("80%", "of inquiries book a consultation, up from 55%")],
        "link": ("/case-studies/plastic-surgery-email", "Read the case study"),
    },
    "quotes": [
        ("We had a booking platform subscription just like everyone else, but it didn't connect to any of our other main systems so we spent so long every day just managing a calendar and a separate CRM. Zoley connected them and now we save 8+ hours a week.", "Sam P.", "Plastic Surgery Office Manager"),
        ("We used to open up in the morning to a pile of texts we'd let sit overnight. Now the system picks them up right away, answers the simple stuff, and flags anything that actually needs one of us. We're not starting every day behind anymore.", "Sasha D.", "Med Spa Practice Owner"),
    ],
    "faq": [
        ("What about patient privacy?", "Patient health information stays in the systems your practice already uses for it. Anything we build that touches patient data is scoped with you before we start, including which tools are allowed to hold it."),
        ("Will replies sound automated?", "They're written in your practice's voice and reviewed with you before anything goes live. Anything that needs clinical judgment or a personal touch goes straight to a coordinator."),
        ("We already have a CRM and a booking platform.", "Good. We connect what you have rather than replace it, so inquiries, bookings, and follow-ups live in one place instead of three."),
        ("How long until something is running?", "Most first builds are live within three to five weeks of the audit, and they run in parallel with your current process before we switch over."),
    ],
    "cta_title": "Let's make sure every inquiry gets the response it deserves.",
    "cta_text": "Tell us how inquiries reach your practice today. We'll come back with a written plan: what we'd build first, why, and what it should return.",
  },

  # ------------------------------------------------------------------ Physical therapy
  {
    "key": "physical-therapy",
    "sid": "zly-ind-physical-therapy",
    "url": "/physical-therapy-practices",
    "tag": "for physical therapy practices",
    "title": "A practice that grows without the owner holding it together.",
    "sub": "Excellent clinical work and loyal patients, and still a ceiling on revenue. We fix the two things that usually cause it: pricing that hasn't kept pace with the care, and operations that live in one person's head.",
    "board": {
        "cards": [("Evaluation", "plan of care set"), ("Tier chosen", "matched to goals"),
                  ("Visit 4 missed", "reminder and rebook"), ("Plan complete", "progress logged")],
        "note": "patients finish what they start",
    },
    "stat": ("~7 in 10", "physical therapy patients don't complete their full plan of care. Every visit they skip is care they don't get and revenue the practice doesn't see."),
    "problems_title": "Why good practices stall.",
    "problems_intro": "When a practice stops growing, the first instinct is to find more patients. Usually the cap is somewhere else.",
    "problems": [
        ("Pricing set once and never revisited.", "One option for every patient, whether they want a check-in or intensive ongoing care. The most valuable work is priced like the simplest."),
        ("Patients drift off before they finish.", "A missed visit becomes two, then the patient is gone. Nobody notices until the schedule has holes in it."),
        ("Follow-up lives in notebooks and texts.", "Histories, reminders, and progress notes spread across paper, phones, and memory. It works until the owner is busy, which is always."),
        ("The owner is the system.", "Every new patient adds weight to one person's day. More demand turns into more pressure instead of more growth."),
    ],
    "builds_title": "What we build for physical therapy practices.",
    "builds_intro": "Strategy first, then the systems that let the practice deliver on it. Most practices start with pricing or retention.",
    "builds": [
        ("Strategy", "Pricing & tier structure", "Clear tiers matched to the different kinds of patients you see, benchmarked against your local market, so higher-touch care is priced like it."),
        ("Automation", "A CRM built around your practice", "One record per patient with history, notes, tier, and next steps, and a daily view of who needs attention. Owned by you, with no extra subscription."),
        ("Automation", "Plan-of-care follow-up", "Missed visits trigger a reminder and an easy rebook, so fewer patients drift off halfway through their care."),
        ("Automation", "Reminders & reactivation", "Appointment reminders, plus a check-in for past patients who might benefit from coming back."),
        ("Web", "A website that brings in the right patients", "Clear about who you help and how, fast on a phone, and set up to be found by people nearby searching for physical therapy."),
        ("AI", "Weekly practice readout", "A plain-language summary of visits, retention, and revenue each week, assembled from the systems you already have."),
    ],
    "proof": {
        "kind": "case",
        "tag": "from our work",
        "title": "A physical therapy practice that grew from $300K to $750K a year.",
        "text": "The practice ran on a single price for every patient, and its operations lived in the owner's head. We built a tiered pricing structure and a custom CRM that lets the practice deliver every tier consistently.",
        "numbers": [("~$750K", "annual revenue, up from ~$300K"), ("55%", "of clients retained at 3+ months, up from 20%"), ("20+ hrs", "of admin time saved every week")],
        "link": ("/case-studies/physical-therapy-practice", "Read the case study"),
    },
    "quotes": [
        ("Zoley helped us understand what our competitors were charging, helped us introduce new offerings, and more than doubled our yearly revenue expectations. We are so happy with the results!!!", "Jack M.", "Physical Therapy Practice Owner"),
    ],
    "faq": [
        ("Does tiered pricing work if we take insurance?", "Tiers suit the cash-pay side of a practice: wellness, performance, and post-discharge programs, or a fully cash-based model. Where payers set the rate, we focus on the other lever: keeping patients through their full plan of care."),
        ("Will raising prices cost us patients?", "Not the way we do it. In our physical therapy engagement the existing option stayed exactly where it was; new tiers went in above it, and patients chose the level of care that fit them."),
        ("Do we need new software?", "Usually not. We build inside the tools you already run. When a practice needs a CRM, we build one around how it works, and the practice owns it outright."),
        ("How long does it take?", "A pricing engagement runs four to six weeks from audit to roadmap. Most automation builds are live within three to five weeks of the audit."),
    ],
    "cta_title": "Let's build the practice you pictured when you opened it.",
    "cta_text": "Tell us how your practice runs today. We'll come back with a written plan: what we'd change first, why, and what it should return.",
  },
]
