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


@pytest.fixture(scope='function')
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
