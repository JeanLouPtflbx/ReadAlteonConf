<html>
<head>
  <title>Read Alteon Config File Tool</title>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="/static/style.css" type="text/css" media="screen" />
  <link rel="icon" type="image/png" href="/static/favicon.png" />
  <link rel="icon" type="image/ico" href="/static/favicon.ico" />
<style media="screen" type="text/css">
body {}
body { font-size: 0.8125em; font-family: "Luxi sans", "Lucida Grande", Lucida, "Lucida Sans Unicode", sans-serif; color: #333; margin: 10px 20px 10px 20px; min-width:550px;}

div.cleaner {
	clear: both;
    height: 33px;
}

div.header { 
    color: #006; 
    background: #eef; 
    padding: 5px 10px 5px 10px; 
    /*border-radius: 10px; */
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
}

h1 { color: #006; background: #eef; padding: 5px 10px 5px 10px; border-radius: 10px;}
h2 { color: #00a; }


a { }
a:link { color: #009; }
a:visited { color: #009; }
a:hover { color: #b00; }
a:active { color: #f00; }

.hidden {
    display: none;
}

label {
    display: block;
    float: left;
    /*width: 180px;*/
    text-align: right;
    margin-right: 15px;
}

textarea, select, #tags_affiches {
    display: block;
    margin-bottom: 5px;
}

fieldset {
    padding: 5px 5px 5px 5px;
    border-radius: 10px;
}

input[type=text], input[type=date], input[type=password], textarea, select    {
    border: 1px solid #999;
    background: #fff;
}

table {
    border: 4px;
    border-collapse: collapse;
    bordercolor: "red" ;
    cellpadding: 10px ;
    vertical-align:middle;
    align: center;
    /*width: 100%;*/
}
table.caption {
    align:left;
}

table,th,td,tr {
    border:2px solid black;
    padding: 3px;
}

th {
    vertical-align:middle;
    align: center;
    background-color: lightgrey;
}
input:focus, textarea:focus, select:focus {
    border: 1px solid #C90;
    box-shadow: 0px 0px 8px rgba(250, 80, 0, 0.3);
}

div.error, .obligatoire {
    background: #fee;
}

div.error {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 10px 10px 10px 10px;
    font-family: "Lucida Console", Monaco, monospace;
}
.footer {
	border-top: 1px solid #dbdbdb;
	padding-top: 10px;
	margin-top: 20px;
	text-align: right;

	color: #006; 
	background: #eef; 
	border-radius: 10px;
	padding: 5px 10px 5px 10px; 
}
</style>

<script type="text/javascript">
  function showHide(divId)
  {
  if (document.getElementById(divId).style.display=="none")
  {
  document.getElementById(divId).style.display="inline";
  }
  else
  {
  document.getElementById(divId).style.display="none";
  }
  }
  
  function show(divId)
  {
  document.getElementById(divId).style.display="block";
  }
  function hide(divId)
  {
  document.getElementById(divId).style.display="none";
  }
</script>

</head>
<body>
<h1>Lecteur de fichier de configuration Alteon</h1>
<fieldset>
    <legend><h2>Utilisation</h2></legend>
    - Charger un fichier de configuration.<br>
    - Selectionner les données à afficher.<br>
    - Travailler !
</fieldset>


% if SFile==True :
<form action="/" enctype="multipart/form-data" method="post" onsubmit="show('legende');hide('erreurs');return(true);">
    <fieldset>
        <legend><h2>Selectionner un fichier de configuration</h2></legend>
        <table width=100%><tr>
            <td align=center bgcolor=#E6E68A>
                <b>Charger un fichier</b>
            </td>
            <td align=center bgcolor=#E6E68A>
                <b>Ajouter un nouveau fichier</b>
            </td>
            <td align=center bgcolor=#E6E68A>
                <b>Supprimer un fichier</b>
            </td>
        </tr>
        <tr><td align=center bgcolor=#FFFFAD>
                <select name="ListeFichiers" size="1">
                    % for file in SelectableFiles :
                        <option value={{file}}>{{file}}</option>
                    % end 
                </select>
            </td>
            <td align=center bgcolor=#FFFFAD>
                <label for="datafile1"> </label>
                <input type="file" name="datafile1" class="obligatoire">
            </td>
            <td align=center bgcolor=#FFFFAD>
                <select name="DelFile" size="1">
                    % for file in SelectableFiles :
                        <option value={{file}}>{{file}}</option>
                    % end 
                </select>
            </td>
        </tr>
        <tr><td colspan=3 align=center bgcolor=#FFFFAD><label for="submit">&nbsp;</label>
                <input type="submit" id="submit" name="submit"></td>
        </tr>
        </table>
    </fieldset>
</form>
% end

% if Fdata == True :
<div id="Fdata">
<form action="/" enctype="multipart/form-data" method="post" onsubmit="show('legende');hide('erreurs');return(true);">
<fieldset>
<legend><h2>Données du fichier : {{ConfigFileName}}</h2></legend>
<table width=100%>
    <tr></tr><td colspan=4 bgcolor=#E68A2E align=center><b>Listing du fichier</b></th></tr>
    <tr>
        <td colspan=4 bgcolor=#FF9933 align=center>
            <textarea  name="FichierConf" cols="90" rows="17" wrap="off" readonly="yes">{{FileContent}}</textarea>
            </fieldset>
        </td>
    </tr>
    <tr>
        <td bgcolor=#E68A2E align=center><b>Reals<br>Liste des Serveurs déclarés</b></th>
        <td bgcolor=#E68A2E align=center><b>Vips<br>Liste des Vips, des ports d'écoutes et des noms associés</b></th>
        <td bgcolor=#E68A2E align=center><b>Filtres <br>Liste des IPs source</b></th>
        <td bgcolor=#E68A2E align=center><b>Filtres <br>Liste des IPs Destination</b></th>
    </tr>
    <tr>
        <td bgcolor=#FF9933 align=center>
            <select name="ListeReals" size="15" multiple="multiple">
                % for IPName in SelectableReals:
                % IP=IPName.split(" ")[0]
                <option value={{IP}}>{{IPName}}</option>
                %end
            </select>
        </td>
        <td bgcolor=#FF9933 align=center>
            <select name="ListeVips" size="15" multiple="multiple">
                % for IP in SelectableVips:
                <option value={{IP}}>{{IP}}</option>
                %end
            </select>
        </td>
        <td bgcolor=#FF9933 align=center>
            <select name="ListeFiltresSIP" size="15" multiple="multiple">
                % for sip in SelectableFiltsSIP:
                <option value={{sip}}>{{sip}}</option>
                %end
            </select>
        </td>
        <td bgcolor=#FF9933 align=center>
            <select name="ListeFiltresDIP" size="15" multiple="multiple">
                % for dip in SelectableFiltsDIP:
                <option value={{dip}}>{{dip}}</option>
                %end
            </select>
        </td>
    </tr>
    <tr></tr><td colspan=4 bgcolor=#E68A2E align=center><b>Vous pouvez selectionner plusieurs objets d'une même liste avec les touches SHIFT et/ou CTRL.</b></th></tr>
    <tr><td bgcolor=#FF9933 align=center colspan=4 ><label for="submit">&nbsp;</label><input type="submit" id="submit" name="submit"></td></tr>
</table>
</fieldset>
</form>
</div>
% end

% if DVips == True :
<div id="DVips">
<fieldset>
<legend><h2>Details des Vips selectionnées</h2></legend>
    Listes des Reals selectioné(s) :
    % for RID in LstReals :
    {{RID}}
    % end
    <br>
    Listes des Vips selectionée(s) ou déduites :
    % for VID in LstVips :
    {{VID}}
    %end
    <br>
    % for VIP in LstVips :
    %   for VID in ListeVips :
    %       if VIP == ListeVips[VID]['vip'] :
    %          IP=ListeVips[VID]['vip']
    %          include('vip.tpl',VID=VID,IP=IP)
    %       end
    %   end
    % end
    
    %# for VID in ListeVips :
    %# IP=ListeVips[VID]['vip']
    %# include('vip.tpl',VID=VID,IP=IP)
    %# end
</div>
% end

% if DFiltres == True :
<div id="DFiltres">
        <fieldset>
        <legend><h2>Details des filtres selectionnés</h2></legend>
        IP source selectionné(s) :
        % for FSRC in LstFiltresSIP :
        {{FSRC}}
        % end
        <br>
        IP destination selectionné(s) :
        % for FDST in LstFiltresDIP :
        {{FDST}}
        % end
        <br>
        <table>
            <tr>
                <td bgcolor=#678167 align=center><b>Filt ID</b></td>
                <td bgcolor=#678167 align=center><b>name</b></td>
                <td bgcolor=#678167 align=center><b>IP source</b></td>
                <td bgcolor=#678167 align=center><b>Action</b></td>
                <td bgcolor=#678167 align=center><b>IP dest</b></td>
            </tr>
            % for FID in ListeFiltres :
            <tr>
                <td align=center bgcolor=#81A181><b>{{FID}}</b></td>
                <td align=center bgcolor=#A6CFA6>{{ListeFiltres[FID]['name']}}</td>
                <td align=right bgcolor=#BFE8BF>{{ListeFiltres[FID]['sip']}}</td>
                <td align=center bgcolor=#CDEECD>{{ListeFiltres[FID]['action']}}</td>
                <td align=left bgcolor=#DCF2DC>{{ListeFiltres[FID]['dip']}}</td>
            </tr>
            % end
        </table>
        </fieldset>
</div>
%end

% if FiltresDoublons == True :
<div id=DoublonFiltres>
    
    <fieldset>
        <legend><h2>Filtres en doublons dans le fichier de configuration</h2></legend>
        <table>
            <tr><th>FiltID</th><th> Nom </th><th>source ip</th><th>action</th><th>destination ip</th></tr>
            % Filt = {}
            % for FID in ListeFiltresDoublons :
            %   Filt['name']=FID.split(";")[0]
            %   Filt['ID']=FID.split(";")[1]
            %   Filt['sip']=FID.split(";")[2]
            %   Filt['action']=FID.split(";")[3]
            %   Filt['dip']=FID.split(";")[4]
            <tr align=center bgcolor=#FF8080><td>{{Filt['ID']}}</td><td>{{Filt['name']}}</td><td>{{Filt['sip']}}</td><td>{{Filt['action']}}</td><td>{{Filt['dip']}}</td></tr>
            % end
        </table>
</div>
%end

%if error:
<div id="erreurs">
    <h2>Erreur lors du traitement du fichier</h2>
    {{!error}}
</div>
%end

<div class="footer">
{{!footer}}
</div>
</body>
</html>
