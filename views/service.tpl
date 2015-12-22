<table class=service>
    <tr class=service>
        <th width=26% class=service colspan="2"><center><b>{{SERVICE}}</b></center></th>
        <td class=service rowspan=2>
            % include('group.tpl',GID=GID,NAME=ListeGroups[GID]['name'],METRIC=ListeGroups[GID]['metric'],HEALTH=ListeGroups[GID]['health'],CONTENT=ListeGroups[GID]['content'],REALS=ListeGroups[GID]['reals'])
            % end
        </td>
    <tr class=service>
        <td class=service>
            <b>rport : </b>{{RPORT}}
            <br><b>pbind : </b>{{PBIND}}
            <br><b>tmout : </b>{{TMOUT}}m
            <br><b>ptmout : </b>{{PTMOUT}}m
            <br><b>cookie : </b>{{COOKIE}}
        </td>
    </tr>
</table>

