import pytest


# %% Url


@pytest.fixture(scope="function")
def clubs_parser_url() -> str:
    return "https://transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2023"


@pytest.fixture(scope="function")
def squads_parser_url() -> str:
    return "https://transfermarkt.co.uk/manchester-united/kader/verein/985/saison_id/2024/plus/1"


@pytest.fixture(scope="function")
def fixtures_parser_url() -> str:
    return "https://www.transfermarkt.co.uk/manchester-united/spielplan/verein/985/saison_id/2024/plus/1#GB1"


@pytest.fixture(scope="function")
def match_lineups_parser_url() -> str:
    return "https://www.transfermarkt.co.uk/manchester-united_liverpool-fc/aufstellung/spielbericht/4361296"


@pytest.fixture(scope="function")
def match_stats_parser_url() -> str:
    return "https://www.transfermarkt.co.uk/manchester-united_liverpool-fc/statistik/spielbericht/4361296"


@pytest.fixture(scope="function")
def match_actions_parser_url() -> str:
    return "https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/4361296"


# %% Html
@pytest.fixture(scope="function")
def clubs_html_sample() -> str:
    return """
    <html>
        <table class="items">
            <tr class="even">
                <td class="zentriert no-border-rechts"><a href="/fc-arsenal/startseite/verein/11/saison_id/2023" title="Arsenal FC"><img alt="Arsenal FC" class="tiny_wappen" src="https://tmssl.akamaized.net//images/wappen/tiny/11.png?lm=1489787850" title="Arsenal FC"/></a></td>
                <td class="hauptlink no-border-links"><a href="/fc-arsenal/startseite/verein/11/saison_id/2023" title="Arsenal FC">Arsenal FC</a> </td>
                <td class="zentriert"><a href="/arsenal-fc/kader/verein/11/saison_id/2023" title="Arsenal FC">40</a></td>
                <td class="zentriert">24.6</td>
                <td class="zentriert">23</td>
                <td class="rechts">€30.08m</td>
                <td class="rechts"><a href="/arsenal-fc/kader/verein/11/saison_id/2023" title="Arsenal FC">€1.20bn</a></td>
            </tr>
        </table>
    </html>
    """


@pytest.fixture(scope="function")
def squads_html_sample() -> str:
    return """
    <html>
        <table class="items">
        <thead>
        <tr>
        <th class="zentriert" id="yw1_c0"><a class="sort-link asc" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/trikotNumber.desc">#</a></th><th id="yw1_c1"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/name">Player</a></th><th class="zentriert" id="yw1_c2"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/dateOfBirthTimestamp">Date of birth/Age</a></th><th class="zentriert" id="yw1_c3">Nat.</th><th class="zentriert" id="yw1_c4"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/size.desc">Height</a></th><th class="zentriert" id="yw1_c5"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/foot.desc">Foot</a></th><th class="zentriert" id="yw1_c6"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/teamMemberSinceTimestamp">Joined</a></th><th class="zentriert" id="yw1_c7">Signed from</th><th class="zentriert" id="yw1_c8"><a class="sort-link" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/contractEndTimestamp">Contract</a></th><th class="rechts" id="yw1_c9"><a class="sort-link desc" href="/manchester-united/kader/verein/985/saison_id/2024/plus/1/sort/marketValueRaw">Market value</a></th></tr>
        </thead>
        <tbody>
        <tr class="odd">
        <td class="zentriert rueckennummer bg_Torwart" title="Goalkeeper"><div class="rn_nummer">24</div></td><td class="posrela">
        <table class="inline-table">
        <tr>
        <td rowspan="2">
        <img alt="André Onana" class="bilderrahmen-fixed lazy lazy" data-src="https://img.a.transfermarkt.technology/portrait/medium/234509-1686929812.jpg?lm=1" src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" title="André Onana"> </img></td>
        <td class="hauptlink">
        <a href="/andre-onana/profil/spieler/234509">
                        André Onana            </a>
        </td>
        </tr>
        <tr>
        <td>
                    Goalkeeper        </td>
        </tr>
        </table>
        </td><td class="zentriert">Apr 2, 1996 (29)</td><td class="zentriert"><img alt="Cameroon" class="flaggenrahmen" src="https://tmssl.akamaized.net//images/flagge/verysmall/31.png?lm=1520611569" title="Cameroon"/></td><td class="zentriert">1,90m</td><td class="zentriert">right</td><td class="zentriert">Jul 20, 2023</td><td class="zentriert"><a href="/inter-mailand/startseite/verein/46/saison_id/2023" title="Inter Milan: Ablöse €50.20m"><img alt="Inter Milan" class="" src="https://tmssl.akamaized.net//images/wappen/verysmall/46.png?lm=1618900989" title="Inter Milan"/></a></td><td class="zentriert">Jun 30, 2028</td><td class="rechts hauptlink"><a href="/andre-onana/marktwertverlauf/spieler/234509">€32.00m</a></td></tr>
    </html>
    """


@pytest.fixture(scope="function")
def fixtures_html_sample() -> str:
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Premier League Information</title>
    <meta charset="UTF-8">
</head>
<body>
    <div class="box"></div>
    <div class="box"></div>
    <div class="box"></div>
    <div class="box">
        <h2 class="content-box-headline content-box-headline--inverted content-box-headline--logo 
        content-box-headline--bottom-bordered content-box-headline--extra-space">
            <a href="/premier-league/startseite/wettbewerb/GB1/saison_id/2024" name="GB1">
                <img alt="Premier League" class="" src="https://tmssl.akamaized.net//images/logo/medium/gb1.png?lm=1521104656" 
                title="Premier League"/>Premier League
            </a>
        </h2>
        <div class="tm-tabs">
            <a class="tm-tab" href="/manchester-united/spielplan/verein/985/saison_id/2024#GB1">
                <div class=""><span>Compact</span></div>
            </a>
            <a class="tm-tab tm-tab__active--parent" href="/manchester-united/spielplan/verein/985/saison_id/2024/plus/1#GB1">
                <div class="tm-tab__active"><span>Detailed</span></div>
            </a>
        </div>
        <div class="responsive-table">
            <table>
                <thead>
                    <tr>
                        <th class="zentriert">Matchday</th>
                        <th class="zentriert">Date</th>
                        <th class="zentriert">Time</th>
                        <th colspan="2">Home team</th>
                        <th colspan="2">Away team</th>
                        <th class="zentriert">System of play</th>
                        <th>Coach</th>
                        <th class="rechts">Attendance</th>
                        <th class="zentriert">Result</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td class="zentriert">
                    <a href="/test/spieltag/wettbewerb/GB1/saison_id/2024/spieltag/1">1</a> </td>
                    <td class="zentriert">
                                                            Fri Aug 16, 2024                                    </td>
                    <td class="zentriert">
                                                            8:00 PM                                    </td>
                    <td class="zentriert no-border-rechts">
                    <a href="/manchester-united/startseite/verein/985"><img alt="Manchester United" class="lazy" 
                    data-src="https://tmssl.akamaized.net//images/wappen/profil/985.png?lm=1457975903" 
                    src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" style="max-width: 15px;" 
                    title="Manchester United"/></a> </td>
                    <td class="no-border-links hauptlink">
                    <a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United">Man Utd</a> <span 
                    class="tabellenplatz">(15.)</span> </td>
                    <td class="zentriert no-border-rechts">
                    <a href="/fulham-fc/startseite/verein/931"><img alt="Fulham FC" class="lazy" 
                    data-src="https://tmssl.akamaized.net//images/wappen/profil/931.png?lm=1556831687" 
                    src="data:image/gif;base64,R0lGODlhAQABAIAAAMLCwgAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" style="max-width: 15px;" 
                    title="Fulham FC"/></a> </td>
                    <td class="no-border-links 1">
                    <a href="/fc-fulham/startseite/verein/931/saison_id/2024" title="Fulham FC">Fulham</a> <span 
                    class="tabellenplatz">(11.)</span> </td>
                    <td class="zentriert">
                                                                4-2-3-1                                        </td>
                    <td><a href="/erik-ten-hag/profil/trainer/3816" id="0" title="Erik ten Hag">Erik ten Hag</a></td>
                    <td class="rechts">
                                                                73.297                                        </td>
                    <td class="zentriert"><a class="ergebnis-link" href="/spielbericht/index/spielbericht/4361261" id="4361261" 
                    title="Match report"><span class="greentext">1:0 </span></a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
    """


@pytest.fixture(scope="function")
def match_lineups_html_sample() -> str:
    return """
<div class="box sb-spielbericht-head">
<div class="direct-headline">
<div class="direct-headline__header-box">
<div class="icons-profil">
<div class="wappen">
<img alt="Premier League" class="" src="https://tmssl.akamaized.net//images/logo/mediumsmall/gb1.png?lm=1521104656"
title="Premier League"> </img></div>
<span class="oddsServe" data-competition="GB1" data-gameday="3" data-match="4361296"></span> <div 
</div>
<div class="box">
<h2 class="content-box-headline content-box-headline--inverted content-box-headline--logo 
content-box-headline--extra-space">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/medium/985.png?lm=1457975903" title="Manchester 
United"/></a>Starting Line-up                    </h2>
<div class="responsive-table">
<table class="items">
<tr>
<td class="zentriert rueckennummer bg_Torwart" title="Goalkeeper">
<div class="rn_nummer">
                  24
                </div>
</td>
<td class="" title="">
<table class="inline-table">
<tr>
<td rowspan="2">
<a href="/andre-onana/profil/spieler/234509">
<img alt="André Onana" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/234509-1686929812.jpg?lm=1" title="André Onana"/>
</a>
</td>
<td><a class="wichtig" href="/andre-onana/leistungsdatendetails/spieler/234509/saison/2024/wettbewerb/GB1" 
title="André Onana">André Onana</a> (28 years old)
                                                    </td>
</tr>
<tr>
<td>Goalkeeper, €35.00m</td>
</tr>
</table>
</td>
<td class="zentriert">
<img alt="Cameroon" class="flaggenrahmen" 
src="https://tmssl.akamaized.net//images/flagge/small/31.png?lm=1520611569" title="Cameroon"/>
</td>
</tr>
</div>
"""


@pytest.fixture(scope="function")
def match_stats_html_sample() -> str:
    return """
<div class="box sb-spielbericht-head">
<div class="direct-headline">
<div class="direct-headline__header-box">
<div class="icons-profil">
<div class="wappen">
<img alt="Premier League" class="" src="https://tmssl.akamaized.net//images/logo/mediumsmall/gb1.png?lm=1521104656"
title="Premier League"> </img></div>
</div>
<div class="spielername-profil">
<h2 class="direct-headline__header">
<span>
<a class="direct-headline__link" href="/premier-league/startseite/wettbewerb/GB1/saison_id/2024" title="Premier 
League">Premier League</a> </span>
</h2>
</div>
</div>
<span class="oddsServe" data-competition="GB1" data-gameday="3" data-match="4361296"></span> <div 
class="arrow-bottom"></div>
<div class="box">
<h2 class="content-box-headline">
        Statistics    </h2>
<div class="unterueberschrift">
        Possession    </div>
<div class="sb-st-ballbesitz">
<a class="sb-st-wappen-heim hide-for-small" href="/manchester-united/startseite/verein/985/saison_id/2024" 
title="Manchester United"><img alt="Manchester United" class="" 
src="https://tmssl.akamaized.net//images/wappen/normquad/985.png?lm=1457975903" title="Manchester United"/></a> <a 
class="sb-st-wappen-gast hide-for-small" href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool 
FC"><img alt="Liverpool FC" class="" src="https://tmssl.akamaized.net//images/wappen/normquad/31.png?lm=1727873452"
title="Liverpool FC"/></a> <div id="yw1"></div> </div>
<div class="unterueberschrift">
        Total shots    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 72.727272727273%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">8</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert-lang" style="width: 100%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-schuss"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">11</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Shots off target    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 45.454545454545%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">5</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 63.636363636364%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-nebenschuss"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">7</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Shots saved    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 0%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">0</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 27.272727272727%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-gehalten"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">3</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Corners    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 45.454545454545%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">5</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 18.181818181818%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-ecke"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">2</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Free kicks    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 63.636363636364%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">7</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 63.636363636364%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-freistoss"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">7</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Fouls    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 63.636363636364%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">7</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 63.636363636364%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-foul"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">7</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
<div class="unterueberschrift">
        Offsides    </div>
<div class="sb-statistik">
<ul>
<li class="sb-statistik-heim">
<div class="sb-statistik-wert" style="width: 0%;background-color: #D9020D;">
<div class="sb-statistik-mitte"></div>
<div class="sb-statistik-zahl" style="color: #fff;">0</div>
<div class="sb-statistik-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-statistik-gast">
<div class="sb-statistik-wert" style="width: 18.181818181818%;background-color: #39403B;">
<div class="sb-statistik-mitte"><span class="sb-sprite sb-stat-abseits"> </span></div>
<div class="sb-statistik-zahl" style="color:#fff;">2</div>
<div class="sb-statistik-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
</div>
"""


@pytest.fixture(scope="function")
def match_actions_html_sample() -> str:
    return """
<div class="box sb-spielbericht-head">
<div class="direct-headline">
<div class="direct-headline__header-box">
<div class="icons-profil">
<div class="wappen">
<img alt="Premier League" class="" src="https://tmssl.akamaized.net//images/logo/mediumsmall/gb1.png?lm=1521104656"
title="Premier League"> </img></div>
</div>
<div class="spielername-profil">
<h2 class="direct-headline__header">
<span>
<a class="direct-headline__link" href="/premier-league/startseite/wettbewerb/GB1/saison_id/2024" title="Premier 
League">Premier League</a> </span>
</h2>
</div>
<span class="oddsServe" data-competition="GB1" data-gameday="3" data-match="4361296"></span> <div 
<div class="box">
<h2 class="content-box-headline">
                Skip</h2>
</div>
<div class="box">
<h2 class="content-box-headline">
                Skip</h2>
</div>
<div class="box">
<h2 class="content-box-headline">
                Goals</h2>
<div class="sb-ereignisse" id="sb-tore">
<ul>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -144px -108px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><b>0:1</b></div>
<div class="sb-aktion-spielerbild">
<a href="/luis-diaz/profil/spieler/480692">
<img alt="Luis Díaz" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/480692-1697903145.jpg?lm=1" title="Luis Díaz"/> </a>
</div>
<div class="sb-aktion-aktion">
<a class="wichtig" href="/luis-diaz/leistungsdatendetails/spieler/480692/saison/2024/wettbewerb/GB1" title="Luis 
Díaz">Luis Díaz</a>, Header, 2. Goal of the Season<br/>
                                    Assist: <a class="wichtig" 
href="/mohamed-salah/leistungsdatendetails/spieler/148455/saison/2024/wettbewerb/GB1" title="Mohamed Salah">Mohamed Salah</a>, Pass, 2. Assist of the Season                                                                        
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -36px -144px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><b>0:2</b></div>
<div class="sb-aktion-spielerbild">
<a href="/luis-diaz/profil/spieler/480692">
<img alt="Luis Díaz" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/480692-1697903145.jpg?lm=1" title="Luis Díaz"/> </a>
</div>
<div class="sb-aktion-aktion">
<a class="wichtig" href="/luis-diaz/leistungsdatendetails/spieler/480692/saison/2024/wettbewerb/GB1" title="Luis 
Díaz">Luis Díaz</a>, Right-footed shot, 3. Goal of the Season<br/>
                                    Assist: <a class="wichtig" 
href="/mohamed-salah/leistungsdatendetails/spieler/148455/saison/2024/wettbewerb/GB1" title="Mohamed Salah">Mohamed Salah</a>, Pass, 3. Assist of the Season                                                                        
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -180px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><b>0:3</b></div>
<div class="sb-aktion-spielerbild">
<a href="/mohamed-salah/profil/spieler/148455">
<img alt="Mohamed Salah" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/148455-1727337594.jpg?lm=1" title="Mohamed Salah"/> </a>
</div>
<div class="sb-aktion-aktion">
<a class="wichtig" href="/mohamed-salah/leistungsdatendetails/spieler/148455/saison/2024/wettbewerb/GB1" 
title="Mohamed Salah">Mohamed Salah</a>, Left-footed shot, 3. Goal of the Season<br/>
                                    Assist: <a class="wichtig" 
href="/dominik-szoboszlai/leistungsdatendetails/spieler/451276/saison/2024/wettbewerb/GB1" title="Dominik 
Szoboszlai">Dominik Szoboszlai</a>, Pass, 2. Assist of the Season                                                  
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
</ul>
</div>
</div>
<div class="box">
<h2 class="content-box-headline">
                Substitutions            </h2>
<div class="sb-ereignisse" id="sb-wechsel">
<ul>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -144px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/casemiro/profil/spieler/16306">
<img alt="Casemiro" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/16306-1699018876.jpg?lm=1" title="Casemiro"/> </a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/toby-collyer/profil/spieler/654253">
<img alt="Toby Collyer" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/654253-1709159230.jpg?lm=1" title="Toby Collyer"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/toby-collyer/leistungsdatendetails/spieler/654253/saison/2024/wettbewerb/GB1" title="Toby Collyer">Toby Collyer</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/casemiro/leistungsdatendetails/spieler/16306/saison/2024/wettbewerb/GB1" 
title="Casemiro">Casemiro</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -216px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/luis-diaz/profil/spieler/480692">
<img alt="Luis Díaz" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/480692-1697903145.jpg?lm=1" title="Luis Díaz"/> </a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/cody-gakpo/profil/spieler/434675">
<img alt="Cody Gakpo" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/434675-1682690965.jpg?lm=1" title="Cody Gakpo"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/cody-gakpo/leistungsdatendetails/spieler/434675/saison/2024/wettbewerb/GB1" title="Cody Gakpo">Cody 
Gakpo</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/luis-diaz/leistungsdatendetails/spieler/480692/saison/2024/wettbewerb/GB1" title="Luis 
Díaz">Luis Díaz</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -288px -216px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/matthijs-de-ligt/profil/spieler/326031">
<img alt="Matthijs de Ligt" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/326031-1700659567.jpg?lm=1" title="Matthijs de Ligt"/> 
</a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/harry-maguire/profil/spieler/177907">
<img alt="Harry Maguire" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/177907-1663841733.jpg?lm=1" title="Harry Maguire"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/harry-maguire/leistungsdatendetails/spieler/177907/saison/2024/wettbewerb/GB1" title="Harry Maguire">Harry 
Maguire</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/matthijs-de-ligt/leistungsdatendetails/spieler/326031/saison/2024/wettbewerb/GB1" 
title="Matthijs de Ligt">Matthijs de Ligt</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite 
sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -288px -216px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/alejandro-garnacho/profil/spieler/811779">
<img alt="Alejandro Garnacho" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/811779-1703629085.jpg?lm=1" title="Alejandro Garnacho"/>
</a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/amad-diallo/profil/spieler/536835">
<img alt="Amad Diallo" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/536835-1694616776.jpg?lm=1" title="Amad Diallo"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/amad-diallo/leistungsdatendetails/spieler/536835/saison/2024/wettbewerb/GB1" title="Amad Diallo">Amad 
Diallo</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/alejandro-garnacho/leistungsdatendetails/spieler/811779/saison/2024/wettbewerb/GB1" 
title="Alejandro Garnacho">Alejandro Garnacho</a><span class="hide-for-small">, Tactical </span><span 
class="sb-sprite sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -252px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/diogo-jota/profil/spieler/340950">
<img alt="Diogo Jota" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/340950-1716296423.jpg?lm=1" title="Diogo Jota"/> </a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/darwin-nunez/profil/spieler/546543">
<img alt="Darwin Núñez" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/546543-1681827179.jpg?lm=1" title="Darwin Núñez"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/darwin-nunez/leistungsdatendetails/spieler/546543/saison/2024/wettbewerb/GB1" title="Darwin Núñez">Darwin 
Núñez</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/diogo-jota/leistungsdatendetails/spieler/340950/saison/2024/wettbewerb/GB1" title="Diogo 
Jota">Diogo Jota</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -252px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/trent-alexander-arnold/profil/spieler/314353">
<img alt="Trent Alexander-Arnold" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/314353-1701680958.jpg?lm=1" title="Trent 
Alexander-Arnold"/> </a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/conor-bradley/profil/spieler/624258">
<img alt="Conor Bradley" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/624258-1708933100.jpg?lm=1" title="Conor Bradley"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/conor-bradley/leistungsdatendetails/spieler/624258/saison/2024/wettbewerb/GB1" title="Conor Bradley">Conor 
Bradley</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/trent-alexander-arnold/leistungsdatendetails/spieler/314353/saison/2024/wettbewerb/GB1" 
title="Trent Alexander-Arnold">Trent Alexander-Arnold</a><span class="hide-for-small">, Tactical </span><span 
class="sb-sprite sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -72px -288px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/andrew-robertson/profil/spieler/234803">
<img alt="Andrew Robertson" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/234803-1709147379.jpg?lm=1" title="Andrew Robertson"/> 
</a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/konstantinos-tsimikas/profil/spieler/338070">
<img alt="Konstantinos Tsimikas" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/338070-1682088468.jpg?lm=1" title="Konstantinos 
Tsimikas"/> </a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/konstantinos-tsimikas/leistungsdatendetails/spieler/338070/saison/2024/wettbewerb/GB1" title="Konstantinos 
Tsimikas">Konstantinos Tsimikas</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/andrew-robertson/leistungsdatendetails/spieler/234803/saison/2024/wettbewerb/GB1" 
title="Andrew Robertson">Andrew Robertson</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite 
sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr"><span class="sb-sprite-uhr-klein" style="background-position: -180px -288px;">
     </span>
</div>
<div class="sb-aktion-spielstand hide-for-small"><span class="sb-sprite sb-wechsel-401" title="Tactical"> 
</span></div>
<div class="sb-aktion-spielerbild">
<a href="/joshua-zirkzee/profil/spieler/435648">
<img alt="Joshua Zirkzee" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/435648-1651087961.jpg?lm=1" title="Joshua Zirkzee"/> 
</a>
</div>
<div class="sb-aktion-aktion">
<div class="sb-aktion-spielerbild">
<a href="/christian-eriksen/profil/spieler/69633">
<img alt="Christian Eriksen" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/69633-1718628122.jpg?lm=1" title="Christian Eriksen"/> 
</a>
</div>
<span class="sb-aktion-wechsel-ein">
<span class="sb-sprite sb-ein"> </span> <a class="wichtig" 
href="/christian-eriksen/leistungsdatendetails/spieler/69633/saison/2024/wettbewerb/GB1" title="Christian 
Eriksen">Christian Eriksen</a> </span>
<span class="sb-aktion-wechsel-aus">
<a class="wichtig" href="/joshua-zirkzee/leistungsdatendetails/spieler/435648/saison/2024/wettbewerb/GB1" 
title="Joshua Zirkzee">Joshua Zirkzee</a><span class="hide-for-small">, Tactical </span><span class="sb-sprite 
sb-aus"> </span>
</span>
</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
</ul>
</div>
</div>
<div class="box">
<h2 class="content-box-headline">
                Cards            </h2>
<div class="sb-ereignisse" id="sb-karten">
<ul>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr">
<span class="sb-sprite-uhr-klein" style="background-position: -72px -72px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><span class="sb-sprite sb-gelb"> </span></div>
<div class="sb-aktion-spielerbild">
<a href="/joshua-zirkzee/profil/spieler/435648">
<img alt="Joshua Zirkzee" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/435648-1651087961.jpg?lm=1" title="Joshua Zirkzee"/></a>
</div>
<div class="sb-aktion-aktion"><a class="wichtig" 
href="/joshua-zirkzee/leistungsdatendetails/spieler/435648/saison/2024/wettbewerb/GB1" title="Joshua 
Zirkzee">Joshua Zirkzee</a><br/>
                                    1. Yellow card  , Foul</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr">
<span class="sb-sprite-uhr-klein" style="background-position: -324px -108px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><span class="sb-sprite sb-gelb"> </span></div>
<div class="sb-aktion-spielerbild">
<a href="/lisandro-martinez/profil/spieler/480762">
<img alt="Lisandro Martínez" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/480762-1680681507.jpg?lm=1" title="Lisandro 
Martínez"/></a>
</div>
<div class="sb-aktion-aktion"><a class="wichtig" 
href="/lisandro-martinez/leistungsdatendetails/spieler/480762/saison/2024/wettbewerb/GB1" title="Lisandro 
Martínez">Lisandro Martínez</a><br/>
                                    1. Yellow card  , Foul</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr">
<span class="sb-sprite-uhr-klein" style="background-position: -144px -144px;">
    +1</span>
</div>
<div class="sb-aktion-spielstand"><span class="sb-sprite sb-gelb"> </span></div>
<div class="sb-aktion-spielerbild">
<a href="/kobbie-mainoo/profil/spieler/820374">
<img alt="Kobbie Mainoo" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/820374-1719349758.jpg?lm=1" title="Kobbie Mainoo"/></a>
</div>
<div class="sb-aktion-aktion"><a class="wichtig" 
href="/kobbie-mainoo/leistungsdatendetails/spieler/820374/saison/2024/wettbewerb/GB1" title="Kobbie Mainoo">Kobbie 
Mainoo</a><br/>
                                    2. Yellow card</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
<li class="sb-aktion-gast">
<div class="sb-aktion">
<div class="sb-aktion-uhr">
<span class="sb-sprite-uhr-klein" style="background-position: -144px -180px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><span class="sb-sprite sb-gelb"> </span></div>
<div class="sb-aktion-spielerbild">
<a href="/virgil-van-dijk/profil/spieler/139208">
<img alt="Virgil van Dijk" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/139208-1702049837.jpg?lm=1" title="Virgil van 
Dijk"/></a>
</div>
<div class="sb-aktion-aktion"><a class="wichtig" 
href="/virgil-van-dijk/leistungsdatendetails/spieler/139208/saison/2024/wettbewerb/GB1" title="Virgil van 
Dijk">Virgil van Dijk</a><br/>
                                    1. Yellow card  , Foul</div>
<div class="sb-aktion-wappen">
<a href="/fc-liverpool/startseite/verein/31/saison_id/2024" title="Liverpool FC"><img alt="Liverpool FC" class="" 
src="https://tmssl.akamaized.net//images/wappen/smallquad/31.png?lm=1727873452" title="Liverpool FC"/></a> </div>
</div>
</li>
<li class="sb-aktion-heim">
<div class="sb-aktion">
<div class="sb-aktion-uhr">
<span class="sb-sprite-uhr-klein" style="background-position: -144px -216px;">
     </span>
</div>
<div class="sb-aktion-spielstand"><span class="sb-sprite sb-gelb"> </span></div>
<div class="sb-aktion-spielerbild">
<a href="/matthijs-de-ligt/profil/spieler/326031">
<img alt="Matthijs de Ligt" class="bilderrahmen-fixed" 
src="https://img.a.transfermarkt.technology/portrait/small/326031-1700659567.jpg?lm=1" title="Matthijs de 
Ligt"/></a>
</div>
<div class="sb-aktion-aktion"><a class="wichtig" 
href="/matthijs-de-ligt/leistungsdatendetails/spieler/326031/saison/2024/wettbewerb/GB1" title="Matthijs de 
Ligt">Matthijs de Ligt</a><br/>
                                    1. Yellow card  , Foul</div>
<div class="sb-aktion-wappen">
<a href="/manchester-united/startseite/verein/985/saison_id/2024" title="Manchester United"><img alt="Manchester 
United" class="" src="https://tmssl.akamaized.net//images/wappen/smallquad/985.png?lm=1457975903" title="Manchester
United"/></a> </div>
</div>
</li>
</ul>
</div>
</div>
"""
