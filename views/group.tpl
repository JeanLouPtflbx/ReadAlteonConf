<table class=group>
        <tr class=group>
            <th width=26% class=group colspan="2"><center><b>{{NAME}}</b><br>group {{GID}}</center></th>
            % for RID in REALS.split():
            <td class=group rowspan="2">    
                %   include('real.tpl',RID=RID,NAME=ListeReals[RID]['name'],ROLE=ListeReals[RID]['role'],INTER=ListeReals[RID]['inter'],RETRY=ListeReals[RID]['retry'],RIP=ListeReals[RID]['rip'])
                % end
            </td>
        </tr>
        <tr class=group >
            <td class=group colspan="2" >
                <b>metric : </b>{{METRIC}}
                <br><b>health : </b>{{HEALTH}}
                <br><b>content : </b>{{CONTENT}}
            </td>
        </tr>
    </table>

