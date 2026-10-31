#!/usr/bin/env python3
"""Builds index.html for pittner/money-vision-board.

A single-purpose page for the "money vision board" / "financial vision board" / "financial goals 2027"
search intent (planned in December and January): 36 goals in 6 groups (saving, debt, budget and
spending, earning more, investing and future, money mindset), each
with why it matters and a first step for this week, and a link that opens the free maker with that
goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098), so it can go on
the phone lock screen. Plus 12 honest money questions, a 45-minute plan, a box for your own goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/money-vision-board/"
SRC = "ghpages_money"
CAMPAIGN = "money_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Saving", [
        ("Save 10% of every paycheck", "Paying yourself first means saving happens before spending, not with what is left.", "Set up an automatic transfer of 10% to savings for the day after payday"),
        ("Build a 3-month emergency fund", "A cushion turns a broken car or a lost job from a crisis into an inconvenience.", "Work out one month of essential costs and open a separate savings account"),
        ("Save for one big thing in cash", "Buying it with saved money feels better and costs less than paying interest.", "Name the thing, its price and the month you want it, then divide"),
        ("Run a no-spend weekend every month", "One weekend without shopping resets habits and shows where money really goes.", "Pick the first no-spend weekend and plan two free things to do"),
        ("Round up every purchase into savings", "Small automatic amounts add up without you noticing the pinch.", "Turn on round-ups in your banking app or move 5 EUR every evening"),
        ("Keep savings in a separate bank", "Money you cannot see in your main app is money you do not spend.", "Open a savings account at a different bank this week"),
    ]),
    ("Debt", [
        ("Pay off my credit card in 2027", "Card interest quietly eats more than almost any investment can earn.", "List the balance and interest rate and set a monthly payment that clears it in 12 months"),
        ("List every debt in one place", "You cannot plan a payoff for debts you avoid looking at.", "Write each debt, its balance, rate and minimum payment on one page tonight"),
        ("Use the snowball: smallest debt first", "Clearing one small debt fast gives you the win that keeps you going.", "Add 20 EUR extra to your smallest debt this month"),
        ("Stop using buy now, pay later", "Split payments make things feel cheaper than they are.", "Remove saved cards from one shopping app today"),
        ("Pay more than the minimum every month", "Minimum payments are designed to keep you in debt for years.", "Add a fixed extra amount to your next payment, even 10 EUR"),
        ("Be debt-free except the mortgage", "No monthly payments means every raise goes to your life, not your past.", "Write the month you want to be free and what you need to pay to get there"),
    ]),
    ("Budget and spending", [
        ("Know where every euro goes", "Most people underestimate their spending by a third until they track it.", "Export last month's bank statement and sort it into five categories"),
        ("Cut three subscriptions I forgot about", "Forgotten subscriptions are money leaving every month for nothing.", "Search your statements for recurring charges and cancel one today"),
        ("Spend 20% less on food delivery", "Delivery is one of the easiest places to save without feeling poorer.", "Check last month's delivery total and set a weekly limit"),
        ("Use a 24-hour rule before buying", "Waiting a day kills most impulse buys before they cost you.", "Put the next non-essential purchase in your cart and decide tomorrow"),
        ("Do a 15-minute money check every Sunday", "A short weekly look keeps small leaks from becoming big problems.", "Put a repeating 15-minute Money Sunday in your calendar"),
        ("Give every euro a job each month", "A plan for the money before the month starts beats guessing at the end.", "Write next month's income and split it into needs, wants and savings"),
    ]),
    ("Earning more", [
        ("Ask for a raise in 2027", "One good conversation can be worth more than a year of cutting coffees.", "Write down three results you delivered this year with numbers"),
        ("Start a side income", "A second income stream makes you safer and speeds up every other goal.", "List three skills people already ask you for help with"),
        ("Earn my first 100 EUR online", "The first 100 proves the idea works and is the hardest one.", "Pick one thing you could sell or offer and tell three people this week"),
        ("Sell what I no longer use", "Unused things are cash sitting in a cupboard.", "Photograph five things you have not used in a year and list them"),
        ("Learn one skill that pays", "A skill employers or clients pay for compounds like money does.", "Choose one course or book and do the first lesson this week"),
        ("Negotiate one bill down", "Insurance, phone and internet providers often lower prices when asked.", "Call or chat with one provider and ask for a better deal"),
    ]),
    ("Investing and future", [
        ("Start investing every month", "Starting small and early matters more than picking the perfect fund.", "Read about low-cost index funds for 30 minutes and pick an amount"),
        ("Increase my pension contribution", "Your future self gets the benefit of every year of compounding.", "Check what you contribute now and what raising it by 1% would cost"),
        ("Understand my net worth", "One number shows if you are moving forward, even when it feels slow.", "Add up what you own and what you owe and write the result with today's date"),
        ("Make a money plan with my partner", "Couples who talk money openly argue about it less.", "Book one calm evening to share your numbers and one goal each"),
        ("Write down my financial freedom number", "A clear target turns saving from a chore into a project.", "Multiply your yearly spending by 25 and write it at the top of your board"),
        ("Learn the basics of taxes", "Knowing the rules can keep hundreds of euros in your pocket.", "Find the two deductions or allowances that apply to you"),
    ]),
    ("Money mindset", [
        ("Stop comparing my money to others", "Comparison spends money you do not have on a life you do not want.", "Mute or unfollow two accounts that make you want to buy things"),
        ("Talk about money without shame", "Money stress grows in silence and shrinks when it is spoken.", "Tell one trusted person one money goal for 2027"),
        ("Celebrate every money win", "Noticing progress keeps you going when the big goal is far away.", "Write down one money thing you did right this month"),
        ("Spend on what I really value", "Spending freely on what matters is easier when you cut what does not.", "Write the three things you love spending on and the three you regret"),
        ("Give regularly, even a little", "Giving makes you feel richer and is a good habit at any income.", "Choose one cause and set a small monthly amount"),
        ("Feel calm, not scared, when I check my account", "Calm comes from a plan, not from a big number.", "Check your balance today and write one sentence about how it feels"),
    ]),
]

QUESTIONS = [
    "How much did I really earn and spend in 2026, roughly?",
    "What did I buy this year that I am glad I did, and what do I regret?",
    "When do I spend money I did not plan to spend, and what is happening then?",
    "What is one money worry that keeps coming back at night?",
    "Who taught me how to think about money, and what did they get wrong?",
    "What would three months of savings change in how I feel?",
    "Which debt bothers me most, and why that one?",
    "What could I earn more for, if I asked or offered it?",
    "What do I want money for, really: safety, freedom, time, experiences?",
    "What is one small money habit I could keep even in a bad month?",
    "Who do I talk to about money, and who should I talk to more?",
    "If 2027 goes really well, what is different about my money by next December?",
]

PLAN = [
    ("10 minutes: look back honestly.", "Open last month's bank statement and write the five biggest categories. The numbers point to your plan."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three goals.", "Not ten. One for saving or debt, one for spending, one for earning more or investing."),
    ("10 minutes: make it visible.", "Turn your most important goal and its first step into a phone lock screen, so you see it every time you open a shopping app."),
]

FAQ = [
    ("What should go on a money vision board?",
     "Put the goal in your own words with a number and a date, a first step you can do this week, and your reason why. "
     "This page has 36 money goals in 6 groups (saving, debt, budget, earning more, investing, mindset), each with a first step, so you can pick three and make them visible."),
    ("Does a financial vision board actually work?",
     "A board does not save money by itself, but seeing your goal every day keeps it in front of you when you decide to spend. "
     "The habit that works best is putting it on your phone lock screen, which you look at right before most purchases."),
    ("How many money goals should I set?",
     "Three is enough: one for saving or paying off debt, one for spending less, and one for earning more or investing. Fewer goals get more attention and stick longer."),
    ("What are realistic financial goals for 2027?",
     "Small and specific beats big and vague: save 10% of every paycheck, build a 3-month emergency fund, pay off the credit card, cancel three forgotten subscriptions, ask for a raise. "
     "Write a number and a month next to each."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full money vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Money Vision Board 2027: %%COUNT%% Financial Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% money and financial goals for 2027 (saving, debt, budget, earning more, investing, mindset), each with a first step for this week, %%NQ%% honest money questions and a 45-minute plan. Turn your goal into a free phone lock screen. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Money vision board 2027 - %%COUNT%% financial goals with a first step and a free lock screen">
<meta property="og:description" content="Saving, debt and income goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Money vision board 2027: %%COUNT%% financial goals with a first step for this week</h1>
  <p class="lede">Most money resolutions fail because the goal has no number, no first step, and is forgotten by February. Below are %%COUNT%% financial goals for saving, debt, spending, earning more and investing, each with why it matters and a first step you can do this week, plus %%NQ%% honest questions about your money in 2026. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every time you are about to buy something. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My money goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Save 3 months of expenses" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Move 10% to savings every payday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% honest money questions before you choose your goals</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your money year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full money vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/money-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
