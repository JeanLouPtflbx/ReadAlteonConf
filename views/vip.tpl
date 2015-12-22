    <table class=vip>
        <tr class=vip>
        <th width=15% class=vip><center><b>{{IP}}</b><br>virt {{VID}}</center></th>
        <td class=vip>
            % for SID in ListeServices[VID]:
            %      include('service.tpl',SID=SID,SERVICE=ListeServices[VID][SID]['service'],RPORT=ListeServices[VID][SID]['rport'],PBIND=ListeServices[VID][SID]['pbind'],TMOUT=ListeServices[VID][SID]['tmout'],PTMOUT=ListeServices[VID][SID]['ptmout'],COOKIE=ListeServices[VID][SID]['cookie'],GID=ListeServices[VID][SID]['group'])
            % end
        </td></tr>
    </table><br>

