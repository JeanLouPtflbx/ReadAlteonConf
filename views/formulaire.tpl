<html>
<head>
  <title>Read Alteon Config File Tool</title>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="stylesheet" href="/static/style.css" type="text/css" media="screen" />
  <link rel="icon" type="image/png" href="/static/favicon.png" />
  <link rel="icon" type="image/ico" href="/static/favicon.ico" />
<style media="screen" type="text/css">

body { 
    font-family: Tahoma, Geneva, Kalimati, sans-serif;
    background: #FFFBE8 ;
    }

fieldset { 
    background: #FFFBE8;
    }

table {
    background : #F0A01F ;
    border: 2px solid #F0761F;
    border-collapse: collapse;
    width:100%;
    align:center;
    }

th, td, tr {
    align: center;
    border: 2px solid #F0761F;
    border-collapse: collapse;
    }

th.vip, tr.vip {border: 2px solid #204878; }
th.group, tr.group {border: 2px solid #204878;}
th.service, tr.service {border: 2px solid #204878;}
th.real, tr.real {border: 2px solid #204878;}

td.filtres, td.vip, td.service, td.group, td.real {background: #FFFBE8 ;}

.vip {
    background : #5F80B5 ;
    border: 2px solid #204878;
    }

.service  {
    background : #6792C5 ;
    border: 2px solid #204878;
    }

.group  {
    background : #94B3C7 ;
    border: 2px solid #204878;
    }

.real  {
    background : #B2C3D5 ;
    border: 2px solid #204878;
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
        <table class="fichier"><tr>
            <th>
                <b>Charger un fichier</b>
            </th>
            <th>
                <b>Ajouter un nouveau fichier</b>
            </th>
            <th>
                <b>Supprimer un fichier</b>
            </th>
        </tr>
        <tr><td>
                <select name="ListeFichiers" size="1">
                    % for file in SelectableFiles :
                        <option value={{file}}>{{file}}</option>
                    % end 
                </select>
            </td>
            <td>
                <label for="datafile1"> </label>
                <input type="file" name="datafile1" class="obligatoire">
            </td>
            <td>
                <select name="DelFile" size="1">
                    % for file in SelectableFiles :
                        <option value={{file}}>{{file}}</option>
                    % end 
                </select>
            </td>
        </tr>
        <tr><td colspan=3><label for="submit">&nbsp;</label>
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
<table class="data">
    <tr></tr><th colspan=4><b>Listing du fichier</b></th></tr>
    <tr>
        <td colspan=4>
            <textarea  name="FichierConf" cols="90" rows="17" wrap="off" readonly="yes">{{FileContent}}</textarea>
            </fieldset>
        </td>
    </tr>
    <tr>
        <th><b>Reals</b><br>Liste des Serveurs déclarés</th>
        <th><b>Vips</b><br>Liste des Vips, des ports d'écoutes et des noms associés</th>
        <th><b>Filtres</b><br>Liste des IPs source</th>
        <th><b>Filtres</b><br>Liste des IPs Destination</th>
    </tr>
    <tr>
        <td>
            <select name="ListeReals" size="15" multiple="multiple">
                % for IPName in SelectableReals:
                % IP=IPName.split(" ")[0]
                <option value={{IP}}>{{IPName}}</option>
                %end
            </select>
        </td>
        <td>
            <select name="ListeVips" size="15" multiple="multiple">
                % for IP in SelectableVips:
                <option value={{IP}}>{{IP}}</option>
                %end
            </select>
        </td>
        <td>
            <select name="ListeFiltresSIP" size="15" multiple="multiple">
                % for sip in SelectableFiltsSIP:
                <option value={{sip}}>{{sip}}</option>
                %end
            </select>
        </td>
        <td>
            <select name="ListeFiltresDIP" size="15" multiple="multiple">
                % for dip in SelectableFiltsDIP:
                <option value={{dip}}>{{dip}}</option>
                %end
            </select>
        </td>
    </tr>
    <tr></tr><td colspan=4><b>Vous pouvez selectionner plusieurs objets d'une même liste avec les touches SHIFT et/ou CTRL.</b></th></tr>
    <tr><td colspan=4 ><label for="submit">&nbsp;</label><input type="submit" id="submit" name="submit"></td></tr>
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
        <table class="filtres">
            <tr class="filtres">
                <th class="filtres"><b>Filt ID</b></th>
                <th class="filtres"><b>name</b></th>
                <th class="filtres"><b>IP source</b></th>
                <th class="filtres" ><b>Action</b></th>
                <th class="filtres"><b>IP dest</b></th>
            </tr>
            % for FID in ListeFiltres :
            <tr class="filtres">
                <td align="center"><b>{{FID}}</b></td>
                <td class="filtres" align="center">{{ListeFiltres[FID]['name']}}</td>
                <td class="filtres" align="right">{{ListeFiltres[FID]['sip']}}</td>
                <td class="filtres" align="center">{{ListeFiltres[FID]['action']}}</td>
                <td class="filtres" align="left">{{ListeFiltres[FID]['dip']}}</td>
            </tr>
            % end
        </table>
        </fieldset>
</div>
%end

% if FiltresDoublons == True :
<div id=DoublonFiltres>
    
    <fieldset>
        <legend><h2>Filtres en doublons</h2></legend>
        <table >
            <tr><th>FiltID</th><th> Nom </th><th>source ip</th><th>action</th><th>destination ip</th></tr>
            % Filt = {}
            % for FID in ListeFiltresDoublons :
            %   Filt['name']=FID.split(";")[0]
            %   Filt['ID']=FID.split(";")[1]
            %   Filt['sip']=FID.split(";")[2]
            %   Filt['action']=FID.split(";")[3]
            %   Filt['dip']=FID.split(";")[4]
            <tr align="center"><td align="center" ><b>{{Filt['ID']}}</b></td><td class="filtres" align="center">{{Filt['name']}}</td><td class="filtres" align="right">{{Filt['sip']}}</td><td class="filtres" align="center">{{Filt['action']}}</td><td class="filtres" align="left">{{Filt['dip']}}</td></tr>
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
