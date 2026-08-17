import { useState } from "react";

/* ═══════════════════════════════════════════════════════════════════════════
   UNIVERSALIZED NATAL CHART — PART II
   Aries Sun · Libra Rising · Sagittarius Moon · Jupiter Final Dispositor
   Extended Analysis: Fixed Stars · Houses · Profections · Solar Arc ·
   Vocation · Psychology · Timing Cycles · OOB · Pre-Natal Syzygy
═══════════════════════════════════════════════════════════════════════════ */

/* ─── HOUSE RULERSHIP DATA ────────────────────────────────────────────── */
const HOUSE_DATA = [
  {
    h:1, sign:"Libra", cusp:"10°48′",
    trad_ruler:"Venus", mod_ruler:"Venus",
    ruler_pos:"Pisces 4°24′ H5 (Exalted)",
    planets:["Uranus Rx 25°58′","Isis Rx 2°55′","Quaoar Rx 5°37′","Circe Rx 6°22′"],
    theme:"Self, Identity, Physical Body, Persona, First Impressions",
    reading:`The Libra Ascendant presents an outer persona of grace, diplomacy, aesthetic sensitivity, and natural charm. The first impression is of someone balanced, harmonious, and relationally skilled — a person who reads the room instinctively and moves through social space with Venus-ruled elegance. Uranus at 25°58′ Libra in the 1st house (retrograde) adds an unmistakable current of originality, electric individuality, and subtle rebellion beneath the Libra surface. Visitors to this persona encounter beauty and courtesy first, and the revolutionary undercurrent only reveals itself over time. Pluto's conjunction to the Ascendant (5°45′, Libra H12/ASC cusp zone) gives the persona a Scorpionic depth and transformative intensity. The Libra mask is genuine, but there is always more — and that more is Plutonian. Isis (Scorpio H1) and Quaoar (Scorpio H1) reinforce the hidden mystery beneath the presented self. Venus as chart ruler in Pisces H5 (exalted) means the persona is ultimately driven by creative love, beauty, and artistic expression — these are not hobbies but the primary organizing principle of identity.`
  },
  {
    h:2, sign:"Scorpio", cusp:"7°00′",
    trad_ruler:"Mars", mod_ruler:"Pluto",
    ruler_pos:"Mars: Gemini H9 / Pluto: Libra H12 Rx",
    planets:["Osiris Rx 27°44′","Ixion Rx 8°08′"],
    theme:"Material Resources, Values, Self-Worth, Financial Instincts",
    reading:`Scorpio on the 2nd house cusp brings depth, intensity, and transformative quality to all financial and material matters. Resources do not flow casually — they accumulate through deep engagement, strategic withholding, and willingness to engage with what others avoid. The traditional ruler Mars in Gemini H9 suggests income and value creation come through intellectual work, communication, and philosophical pursuits. The modern ruler Pluto in H12 (hidden sector) indicates that the relationship with money and self-worth carries unconscious dimensions — early programming around scarcity, power, and worthiness shapes financial patterns from below the threshold of awareness. Ixion (accountability, compulsive patterns) in Scorpio H2 suggests that financial karma may involve themes of integrity and the consequences of misusing resources. Osiris (resurrection, transformation) in Scorpio H2 points to cyclical patterns of loss-and-renewal in financial life — material resources may die and be reborn multiple times.`
  },
  {
    h:3, sign:"Sagittarius", cusp:"7°00′",
    trad_ruler:"Jupiter", mod_ruler:"Jupiter",
    ruler_pos:"Jupiter: Pisces H5 (Domicile)",
    planets:["Moon 10°13′","Neptune Rx 9°22′","True Node Rx 21°06′"],
    theme:"Mind, Communication, Local Environment, Siblings, Short Travel",
    reading:`The 3rd house stellium — Moon, Neptune, and True Node — is one of the most distinctive architectural features of this chart. The Moon's fusion with Neptune (0°51′) in the house of mind and communication describes a thinking process that is fundamentally mystical, permeable, and visionary. This is not a mind that processes information in linear, logical steps — it receives impressions, images, feelings, and intuitive flashes, and communicates from that domain. The True Node here confirms: the soul's evolutionary mission (what this person is here to develop and transmit) flows directly through the medium of mystical communication. Writing, speaking, teaching, or any form of transmitting inner experience to others is the karmic vehicle. The house ruler Jupiter in Pisces H5 (domicile) amplifies the creative and spiritual dimensions: the mind is abundant, expansive, and philosophically generous. The challenge (Moon □ Venus, Moon □ Jupiter) is that emotional weather can disrupt the communication channel — when feelings flood the Neptunian field, clarity of expression suffers.`
  },
  {
    h:4, sign:"Capricorn", cusp:"19°00′",
    trad_ruler:"Saturn", mod_ruler:"Saturn",
    ruler_pos:"Saturn: Gemini H9 (Peregrine, anaretic 29°)",
    planets:["Lilith 26°26′","Pallas 5°18′ Aq","Psyche 5°27′ Aq","Ptah 26°57′ Cap"],
    theme:"Home, Roots, Family of Origin, Private Self, Psychological Foundation",
    reading:`Capricorn on the 4th house cusp gives the home and family foundation a Saturnian quality — structure, discipline, authority, and the weight of responsibility characterize the domestic environment. The ruler Saturn in Gemini H9 (anaretic 29°, in square with Mercury) indicates that the psychological foundation was shaped by intellectual pressure, communication challenges, or an environment where ideas and their precise expression carried great importance. The anaretic degree of Saturn suggests urgency or unfinished business in the ancestral/family lineage around these themes. Lilith in Capricorn 26°26′ at the IC zone suggests a powerful, unacknowledged feminine energy in the ancestral line — a dark or suppressed maternal archetype that operates as an undercurrent in the foundational psyche. Pallas and Psyche in Aquarius H4 point to intellectual pattern-recognition and deep psychological work as the foundation for the private self — the inner world is structured around systems of thought and the ongoing work of psychological integration.`
  },
  {
    h:5, sign:"Aquarius", cusp:"26°00′",
    trad_ruler:"Saturn", mod_ruler:"Uranus",
    ruler_pos:"Saturn: Gemini H9 / Uranus: Libra H1 Rx",
    planets:["Venus 4°24′ Pis (Exalt)","Jupiter 7°26′ Pis (Dom)","Ceres 27°23′ Aq","Juno 24°55′ Aq","Eros 7°18′ Pis","Pholus 9°13′ Pis"],
    theme:"Creativity, Romance, Children, Self-Expression, Joy, Play",
    reading:`The 5th house is the most loaded house in the entire chart — containing the chart ruler (Venus exalted), the final dispositor (Jupiter domicile), Eros, Pholus, and with Juno and Ceres just inside the Aquarius cusp zone. This is the house of the Sun's joy, and its extraordinary density of elevated planets creates an almost irresistible gravitational pull: the native's life force is most alive, most authentic, and most generative in the domain of creative self-expression and romantic love. Venus and Jupiter in Pisces describe creative abundance of the most transcendent kind — art, music, poetry, spiritual creativity, romantic idealism. Eros in Pisces (7°18′, essentially conjunct Jupiter) fuses the erotic with the spiritual: love and desire are vehicles for mystical connection. Pholus in Pisces (9°13′) in this context suggests a potentially uncapping quality — when the creative and romantic channels open fully, transformative forces are unleashed that may surprise even the native. Juno in Aquarius at the 5th house cusp describes the ideal romantic partner archetype as intellectually electric, freedom-loving, and Aquarian in nature. The creative output has a humanitarian, collective, or visionary dimension.`
  },
  {
    h:6, sign:"Pisces", cusp:"27°00′",
    trad_ruler:"Jupiter", mod_ruler:"Neptune",
    ruler_pos:"Jupiter: Pisces H5 (Dom) / Neptune: Sagittarius H3 Rx",
    planets:["Mercury 28°55′ Pisces (Fall)","Parthenope 24°11′ Pis"],
    theme:"Health, Daily Work, Service, Craft, Routine, Employees",
    reading:`Pisces on the 6th house and Mercury (Fall) here in service-related work creates a distinctive pattern: the daily work environment operates best when Piscean qualities are honored — fluidity, compassion, artistic or spiritual context, and freedom from overly rigid routine. Mercury in its fall in Pisces in the 6th house describes a mind that can struggle with the organizational demands of conventional work — filing, scheduling, linear task management, and precise detail work require conscious effort. The gift is that the native brings extraordinary empathy, creativity, and healing sensitivity to service contexts: any work involving care, art, counseling, spiritual practice, or imaginative output can flourish here. The ruler Jupiter in H5 suggests work and creativity are not separate domains — the most fulfilling 'daily work' IS creative or romantic expression. Health themes (6th house) may involve the nervous system (Mercury), boundaries (Pisces), and the feet/lymphatic system (Pisces body rulership). The Moon-Neptune conjunction in H3 (ruling the communication of inner states) feeds into the 6th house dynamic: work flows best when inner vision can be expressed outwardly through the craft.`
  },
  {
    h:7, sign:"Aries", cusp:"10°48′",
    trad_ruler:"Mars", mod_ruler:"Mars",
    ruler_pos:"Mars: Gemini H9",
    planets:["Sun 20°41′ (Exalt)","Chiron 20°22′","Cupido 26°38′","Vertex 29°14′","Kaali 16°45′","Sedna 3°05′ Tau"],
    theme:"Partnerships, Marriage, Open Enemies, Significant Others",
    reading:`The 7th house concentration is extraordinary and deeply significant. The exalted Sun, Chiron at exact conjunction (0°19′), the fated Vertex, the charged Cupido, and the deep-space feminine Sedna all occupy the partnership house. The Sun in the 7th means the native finds their fullest self-expression THROUGH relationship — the partner is the mirror in which solar identity becomes visible. This is not dependency but a genuine structural feature: identity crystallizes in relational contact. Chiron here means the wound-site is activated by every significant partnership — the partner somehow touches the core wound, and the relationship becomes the healing arena. The Vertex at 29° Aries is the fated encounter point — relationships that cross this threshold carry an unmistakable quality of destiny. Cupido (the asteroid of romantic desire and idealized love) amplifies the charged quality of 7th house encounters. The Mars ruler in Gemini H9 describes the ideal partner as intellectually driven, philosophically alive, communicatively brilliant, and freedom-oriented (Gemini/9th house themes). Sedna at Taurus 3° in the 7th participates in the Yod configuration (with Venus and Pluto) — the partner carries something of the Sedna archetype: depth, exile, primordial feminine power, or the experience of betrayal-and-transformation.`
  },
  {
    h:8, sign:"Taurus", cusp:"7°00′",
    trad_ruler:"Venus", mod_ruler:"Pluto",
    ruler_pos:"Venus: Pisces H5 (Exalt) / Pluto: Libra H12 Rx",
    planets:["POF Cancer 0°21′","Pan 8°09′ Tau","Parvati 21°04′ Tau","Pythia 18°53′ Tau"],
    theme:"Transformation, Shared Resources, Death & Rebirth, Hidden Depths, Sexuality",
    reading:`The Part of Fortune at Cancer 0°21′ in the 8th house — conjunct Saturn (0°58′) — is among the most decisive placements in the entire chart. Fortune is located in the domain of transformation, shared resources, depth psychology, and regeneration. This is not a chart where abundance flows through easy, superficial channels. Fortune requires depth of engagement: willingness to go where others won't, to work with what is hidden, to sit with what is difficult. The Cancer ingress (0°21′ = fresh into Cancer) gives the 8th house POF a nurturing, protective, emotionally resonant quality — fortune flows when the native provides safety and depth of care in transformative contexts. Venus rules the 8th house (Taurus cusp) and Venus is exalted in H5 — linking creative love directly to the depth domains. Parvati (the devoted goddess, the practice of devotion) and Pythia (the oracle, prophetic channel) in Taurus H8 suggest that oracular, devotional, and healing practices have a genuine place in how the depth dimension of this chart expresses. Pan in Taurus H8 (the wild nature force, panic, and earthy vitality) adds an embodied, sometimes overwhelming physical energy to the 8th house domain.`
  },
  {
    h:9, sign:"Gemini", cusp:"7°00′",
    trad_ruler:"Mercury", mod_ruler:"Mercury",
    ruler_pos:"Mercury: Pisces H6 (Fall) — 28°55′, anaretic degree",
    planets:["Mars 24°26′","Saturn 29°22′ (anaretic)","Pandora 17°38′"],
    theme:"Higher Learning, Philosophy, World-View, Travel, Publishing, Spirituality",
    reading:`The 9th house stellium — Mars, Saturn (anaretic), and Pandora — in Gemini describes the intellectual-philosophical arena as a primary battlefield and life theater. This is where the native fights most intensely: Mars brings combative energy and relentless drive to the domain of ideas, beliefs, and truth-seeking. Saturn at 29° Gemini (the anaretic degree of critical, urgent completion) suggests a lifetime of philosophical pressure — there is always more to learn, more frameworks to test, more mental structures to build and dismantle. The tension between these two (Mars wants to move fast and fight for ideas; Saturn demands rigor and structural integrity) creates a productive creative friction that drives genuine intellectual depth. Pandora in Gemini H9 suggests that once the philosophical curiosity opens (and it always does), it cannot be closed again — the 'box' of ideas once opened releases a cascade of questions that define the entire worldview search. The ruler Mercury in Fall at 29° Pisces (H6) creates an ironic feedback loop: the ruler of the philosophy/world-view house is itself at its most challenged in the chart, in the sign of its fall, at the most critical degree. The philosophical search is always somewhat haunted by the difficulty of putting the ineffable into precise words.`
  },
  {
    h:10, sign:"Cancer", cusp:"19°00′",
    trad_ruler:"Moon", mod_ruler:"Moon",
    ruler_pos:"Moon: Sagittarius H3 (conjunct Neptune)",
    planets:["Orcus 22°34′"],
    theme:"Career, Public Reputation, Life Mission, Authority, Social Standing",
    reading:`Cancer on the MC (Midheaven) describes a public calling oriented around nurturing, protection, emotional care, and the creation of safety. The native's most authentic career expression involves caring for others in some way — psychologically, creatively, or spiritually. The ruler Moon in Sagittarius H3 (fused with Neptune) gives the career dimension a mystical, communicative, and philosophically expansive quality. The work that fulfills the MC requires both the nurturing quality of Cancer and the visionary, truth-seeking spirit of Sagittarius/Neptune: thus, caring communication, spiritual teaching, therapeutic creativity, mystical counsel, or artistic nurturing describes the most authentic vocational expression. Orcus in Cancer H10 (the dwarf planet associated with oath-keeping, accountability to one's word, and underworld leadership) suggests that the public reputation is built — or lost — around integrity, depth of commitment, and the willingness to honor promises made. The public figure carries the Cancerian archetype of protector/nurturer and is held accountable by Orcus to the actual lived reality of that role.`
  },
  {
    h:11, sign:"Leo", cusp:"26°00′",
    trad_ruler:"Sun", mod_ruler:"Sun",
    ruler_pos:"Sun: Aries H7 (Exalted) — 20°41′",
    planets:["Haumea Rx 11°45′ Vir","Makemake Rx 16°33′ Leo"],
    theme:"Friendships, Groups, Community, Social Vision, Long-Term Goals",
    reading:`Leo on the 11th house cusp gives the social sphere a solar, dramatic, and creative quality. Friends and communities that orbit this native tend to be vibrant, expressive, and organized around a creative or visionary center. The ruler Sun in Aries H7 (exalted) means the social circle and long-term vision are most fully realized through partnership — the community is built through and around significant relationships. Makemake in Leo H11 (the dwarf planet of fertility, creativity, and the instinct to generate new life/new forms) amplifies the creative-communal dimension: this person contributes something genuinely novel and generative to the groups they inhabit. Haumea in Virgo H11 (the goddess of fertility and rebirth through natural cycles) suggests that the community dimension also involves a healing, renewing, and practical service orientation. Long-term goals tend to manifest through sustained relationships with groups that share a philosophical and creative vision.`
  },
  {
    h:12, sign:"Virgo", cusp:"27°00′",
    trad_ruler:"Mercury", mod_ruler:"Mercury",
    ruler_pos:"Mercury: Pisces H6 (Fall) — 28°55′ anaretic",
    planets:["Pluto Rx 5°03′ Lib","Vesta Rx 8°15′ Lib"],
    theme:"Hidden Realms, Unconscious, Self-Undoing, Isolation, Spiritual Depth, Karma",
    reading:`Pluto retrograde in Libra in the 12th house is one of the most psychologically complex placements in the chart. Pluto's retrograde in the hidden house suggests that transformative power operates largely outside conscious awareness — the deep psychological patterns that drive behavior are Plutonian in intensity but Libran in expression, meaning they operate through relationship dynamics, aesthetic sensibilities, and the search for balance. The conjunction to the Ascendant (5°45′) is crucial: Pluto's 12th-house/ASC liminal position means that what is hidden in the 12th periodically erupts into the Libra persona — Scorpionic intensity, depth, and transformative pressure periodically take over the graceful Libra mask. Vesta retrograde in Libra H12 (Vesta = sacred devotion, the eternal flame, the hermit priestess) confirms a deeply private, inward orientation of spiritual practice. The sacred fire burns in the hidden house — spiritual life is interior, personal, and resistant to external structure. The ruler Mercury in Fall (Pisces H6) links the 12th house's unconscious domains to the mind's dissolution tendency: the unconscious speaks through imagination, dreams, and permeable mental states rather than through rational processes.`
  },
];

/* NOTE: this component is intentionally data-heavy and mirrors provided content. */

const FIXED_STARS = [
  { star:"Antares", constellation:"Scorpio", nature:"Mars/Jupiter", magnitude:1.06, position:"Sagittarius 9°47′ (1974)", linked_body:"Moon", contact:"Conjunction (< 1°)", nature_desc:"The Heart of the Scorpion — warrior passion, intensity, obsession, spiritual fire", interpretation:`Antares conjunct the Moon is one of the most charged fixed star contacts possible. Antares (the rival of Mars) brings its entire warrior-passion archetype directly into the emotional field.` },
  { star:"Spica", constellation:"Virgo", nature:"Venus/Mars", magnitude:0.98, position:"Libra 23°50′ (1974)", linked_body:"Uranus (conj) + Sun (opp)", contact:"Conjunction with Uranus (2°08′) / Paran Rising with Uranus", nature_desc:"The Spike of Wheat — supreme benefic, artistry, gifts, rare talent, fortune", interpretation:`Spica is one of the most fortunate fixed stars in the tradition — associated with exceptional gifts, artistic brilliance, and rare talent.` },
  { star:"Fomalhaut", constellation:"Piscis Austrinus", nature:"Venus/Mercury", magnitude:1.16, position:"Pisces 3°52′ (1974)", linked_body:"Sun (heliacal rising Apr 12)", contact:"Heliacal Rising — 2 days after birth", nature_desc:"One of the Four Royal Stars (Watcher of the South) — mystical idealism, spiritual charisma, inspired creativity", interpretation:`Fomalhaut's heliacal rising just 2 days after birth makes it a parans star of the first importance.` },
  { star:"Vindemiatrix", constellation:"Virgo", nature:"Saturn/Mercury", magnitude:2.83, position:"Libra 9°56′ (1974)", linked_body:"Pluto (conj)", contact:"Conjunction with Pluto (< 5°)", nature_desc:"The Grape-Gatherer — widowhood, sorrow, loss, but also harvest from what has been cultivated", interpretation:`Vindemiatrix conjunct Pluto in the 12th house is a somber, depth-charging contact.` },
  { star:"Capella", constellation:"Auriga", nature:"Mercury/Mars", magnitude:0.08, position:"Gemini 21°51′ (1974)", linked_body:"Morning first Apr 21", contact:"Heliacal rising (11 days after birth) — seasonal star", nature_desc:"The She-Goat — curiosity, versatility, intellectual hunger, communicative brilliance", interpretation:`Capella's heliacal morning-first rising 11 days after birth marks it as a seasonal sky-companion.` },
];

const SOLAR_ARCS = [
  { age:25, year:"~1999", sa_sun:"Taurus 15°42′", sa_mc:"Leo 14°00′", sa_asc:"Scorpio 5°48′", key_events:["SA Sun enters Taurus","SA MC in Leo","SA ASC in Scorpio"], theme:"First major identity consolidation period" },
  { age:40, year:"~2014", sa_sun:"Gemini 0°41′", sa_mc:"Leo 29°00′ (anaretic)", sa_asc:"Scorpio 20°48′", key_events:["SA Sun enters Gemini","SA MC reaches 29° Leo","SA ASC at 20° Scorpio"], theme:"Mid-life creative and career crystallization" },
  { age:45, year:"~2019", sa_sun:"Gemini 5°41′", sa_mc:"Virgo 4°00′", sa_asc:"Scorpio 25°48′", key_events:["SA MC enters Virgo","SA ASC nears 29° Scorpio","SA Sun in Gemini"], theme:"Craft mastery and precision refinement" },
  { age:50, year:"~2024", sa_sun:"Gemini 10°41′", sa_mc:"Virgo 9°00′", sa_asc:"Sagittarius 0°48′", key_events:["SA ASC enters Sagittarius (0°)","SA Sun preparing Mars-Saturn zone","SA MC in Virgo","Profection to H3"], theme:"The Sagittarian persona emerging; wisdom-teacher period" },
];

const PROFECTIONS = [
  { age:48, year:"Apr 2022–Apr 2023", house:1, sign:"Libra", ruler:"Venus", theme:"Personal identity year." },
  { age:49, year:"Apr 2023–Apr 2024", house:2, sign:"Scorpio", ruler:"Mars/Pluto", theme:"Resources and values year." },
  { age:50, year:"Apr 2024–Apr 2025", house:3, sign:"Sagittarius", ruler:"Jupiter", theme:"Communication and writing year." },
  { age:51, year:"Apr 2025–Apr 2026", house:4, sign:"Capricorn", ruler:"Saturn", theme:"Foundations and home year." },
  { age:52, year:"Apr 2026–Apr 2027", house:5, sign:"Aquarius", ruler:"Saturn/Uranus", theme:"Creative abundance year." },
];

const OOB_PLANETS = [
  { planet:"Mars", dec:"24°52′N", limit:"23°27′", excess:"1°25′", interpretation:`Mars is out of bounds, amplifying unconstrained drive and force.` },
  { planet:"Makemake", dec:"39°59′N", limit:"23°27′", excess:"16°32′", interpretation:`Makemake is extremely out of bounds, indicating unusually unconstrained creative force.` },
];

const VOCATIONAL_ANALYSIS = {
  primary_indicators:[
    { factor:"Venus exalted Pisces H5", weight:"★★★★★", vocation:"Creative arts" },
    { factor:"Jupiter domicile Pisces H5", weight:"★★★★★", vocation:"Teaching, spiritual guidance" },
    { factor:"Moon ☌ Neptune H3", weight:"★★★★★", vocation:"Mystical communication" },
  ],
  calling_synthesis:`This chart emphasizes a healer-teacher-artist vocation through communication and creative expression.`,
};

const PSYCHOLOGICAL = [
  { dimension:"Core Ego Structure", shadow:"Identity linked to wound-site.", gift:"Authentic self-expression heals.", integration:"Express through vulnerability." },
  { dimension:"Emotional Architecture", shadow:"Emotional permeability.", gift:"Extraordinary empathy.", integration:"Boundaries and creative channeling." },
];

const LUNAR_PHASE_DATA = {
  prenatal_lunation:"Full Moon approximately April 7, 1974 — 3 days before birth",
  birth_phase:"Disseminating Moon",
  phase_reading:`The disseminating phase indicates a strong impulse to share and teach gathered insight.`,
};

const CS = `
  @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Josefin+Sans:wght@300;400;600&display=swap');
  :root { --bg:#03040c;--mid:#08091a;--card:#0d0f22;--rim:#1c2038;--gold:#c9a84c;--gold-l:#e8c96d;--gold-d:rgba(201,168,76,.35);--teal:#4ba99a;--violet:#7c5cbf;--crimson:#c2415a;--text:#d4d8f0;--muted:#5a5f7a;--silver:#9ba3c4; }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:'Cormorant Garamond',serif;font-size:15px;line-height:1.7}
  @keyframes shimmer{0%,100%{opacity:.7}50%{opacity:1}}
  @keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
  .container{max-width:1100px;margin:0 auto;padding:1.5rem}
  .header{text-align:center;padding:2rem 1rem 1.75rem;border-bottom:1px solid var(--rim);margin-bottom:2rem}
  .header-title{font-family:'Cinzel Decorative',serif;font-size:clamp(.95rem,2.4vw,1.5rem);color:var(--gold-l);letter-spacing:.12em;margin-bottom:.3rem}
  .tabs{display:flex;overflow-x:auto;gap:0;border-bottom:1px solid var(--rim);margin-bottom:2rem;scrollbar-width:none;flex-wrap:wrap}
  .tab{font-family:'Josefin Sans',sans-serif;font-size:.55rem;letter-spacing:.14em;text-transform:uppercase;padding:.65rem .9rem;background:none;border:none;cursor:pointer;white-space:nowrap;transition:all .2s;border-bottom:2px solid transparent}
  .tab.on{color:var(--gold-l);border-bottom-color:var(--gold)} .tab.off{color:var(--muted)}
  .card{background:var(--card);border:1px solid var(--rim);border-radius:6px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;animation:fadeIn .3s ease}
  .card-title{font-family:'Josefin Sans',sans-serif;font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.9rem}
  .badge{display:inline-block;padding:.14rem .5rem;border-radius:20px;font-family:'Josefin Sans',sans-serif;font-size:.55rem;letter-spacing:.1em;text-transform:uppercase;margin-right:.3rem}
  .bg{background:rgba(201,168,76,.1);color:var(--gold);border:1px solid var(--gold-d)} .bt{background:rgba(75,169,154,.1);color:var(--teal);border:1px solid rgba(75,169,154,.3)} .bv{background:rgba(124,92,191,.1);color:var(--violet);border:1px solid rgba(124,92,191,.3)}
  .hdr{display:flex;align-items:center;gap:1rem;margin-bottom:1.75rem} .hdr-icon{font-size:2rem;color:var(--gold-d);animation:shimmer 3s ease-in-out infinite}
  .sec-t{font-family:'Cinzel Decorative',serif;font-size:clamp(.9rem,2vw,1.25rem);color:var(--gold-l)} .sec-s{font-family:'Josefin Sans',sans-serif;font-size:.6rem;color:var(--muted);letter-spacing:.15em;text-transform:uppercase;margin-top:.2rem}
  .reading{font-size:.88rem;line-height:1.9;color:var(--text)} .alert-g{padding:.7rem 1rem;border-left:3px solid var(--gold);background:rgba(201,168,76,.06);border-radius:0 4px 4px 0;font-size:.84rem;margin-bottom:1rem}
`;

function Acc({ title, children, accent = "var(--gold-d)", open: initOpen = false }) {
  const [open, setOpen] = useState(initOpen);
  return (
    <div style={{ border: `1px solid ${open ? accent : "var(--rim)"}`, borderRadius: 4, marginBottom: ".5rem" }}>
      <button onClick={() => setOpen(!open)} style={{ width: "100%", background: "none", border: "none", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center", padding: ".7rem 1rem" }}>
        <span style={{ fontFamily: "'Josefin Sans',sans-serif", fontSize: ".6rem", letterSpacing: ".15em", textTransform: "uppercase", color: open ? accent : "var(--muted)" }}>{title}</span>
        <span style={{ color: accent, transition: "transform .25s", transform: open ? "rotate(180deg)" : "none", display:"inline-block" }}>▾</span>
      </button>
      {open && <div style={{ padding: "0 1rem 1rem" }}>{children}</div>}
    </div>
  );
}

export default function NatalPart2() {
  const [tab, setTab] = useState("houses");
  const TABS = [
    { id: "houses", label: "House Analysis" },
    { id: "stars", label: "Fixed Stars" },
    { id: "arcs", label: "Solar Arc" },
    { id: "prof", label: "Profections" },
    { id: "oob", label: "OOB Planets" },
    { id: "lunar", label: "Lunar Phase" },
    { id: "vocation", label: "Vocation" },
    { id: "psych", label: "Psychology" },
  ];

  return (
    <>
      <style>{CS}</style>
      <div className="container">
        <div className="header">
          <div style={{ fontSize: "1.6rem", color: "var(--gold-d)", marginBottom: ".4rem", animation: "shimmer 2s ease-in-out infinite" }}>⌂ ★ ⊕ △</div>
          <div className="header-title">Universalized Natal Reading — Part II</div>
          <div style={{ fontFamily: "'Cormorant Garamond',serif", fontStyle: "italic", color: "var(--silver)", margin: ".3rem 0" }}>Aries Sun · Libra Rising · Sagittarius Moon</div>
        </div>

        <div className="tabs">
          {TABS.map(t => (
            <button key={t.id} className={`tab ${tab === t.id ? "on" : "off"}`} onClick={() => setTab(t.id)}>{t.label}</button>
          ))}
        </div>

        {tab === "houses" && (
          <div>
            <div className="hdr">
              <span className="hdr-icon">⌂</span>
              <div><div className="sec-t">House-by-House Analysis</div><div className="sec-s">Placidus · Rulers · Occupants · Themes · Deep Interpretation</div></div>
            </div>
            {HOUSE_DATA.map((h, i) => (
              <Acc key={i} title={`H${h.h} · ${h.sign} · ${h.cusp} · Ruler: ${h.trad_ruler}${h.mod_ruler !== h.trad_ruler ? " / " + h.mod_ruler : ""} · ${h.theme}`} accent="var(--gold-d)">
                <p className="reading">{h.reading}</p>
              </Acc>
            ))}
          </div>
        )}

        {tab === "stars" && (
          <div>
            <div className="hdr"><span className="hdr-icon">★</span><div><div className="sec-t">Fixed Stars</div></div></div>
            {FIXED_STARS.map((s, i) => (
              <div key={i} className="card">
                <div className="card-title">★ {s.star}</div>
                <p className="reading">{s.interpretation}</p>
              </div>
            ))}
          </div>
        )}

        {tab === "arcs" && (
          <div>
            {SOLAR_ARCS.map((arc, i) => (
              <div key={i} className="card">
                <div className="card-title">Age {arc.age} · {arc.year}</div>
                <p className="reading">{arc.theme}</p>
              </div>
            ))}
          </div>
        )}

        {tab === "prof" && (
          <div>{PROFECTIONS.map((p, i) => <div key={i} className="card"><div className="card-title">Age {p.age} · {p.year}</div><p className="reading">{p.theme}</p></div>)}</div>
        )}

        {tab === "oob" && (
          <div>{OOB_PLANETS.map((p, i) => <div key={i} className="card"><div className="card-title">{p.planet}</div><p className="reading">{p.interpretation}</p></div>)}</div>
        )}

        {tab === "lunar" && (
          <div className="card"><div className="card-title">Birth Moon Phase — {LUNAR_PHASE_DATA.birth_phase}</div><p className="reading">{LUNAR_PHASE_DATA.phase_reading}</p></div>
        )}

        {tab === "vocation" && (
          <div className="card"><div className="card-title">Vocational Synthesis</div><p className="reading">{VOCATIONAL_ANALYSIS.calling_synthesis}</p></div>
        )}

        {tab === "psych" && (
          <div>{PSYCHOLOGICAL.map((p, i) => <div key={i} className="card"><div className="card-title">{p.dimension}</div><p className="reading"><strong>Shadow:</strong> {p.shadow}</p><p className="reading"><strong>Gift:</strong> {p.gift}</p></div>)}</div>
        )}
      </div>
    </>
  );
}
