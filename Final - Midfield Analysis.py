# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Import modules
import pandas as pd
import numpy as np
from mplsoccer import Sbopen, VerticalPitch
from matplotlib import rcParams
import matplotlib.pyplot as plt

# Set the font and the plot resolution
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['figure.dpi'] = 300

# Set StatsBomb API IDs
comp_id = 55 # Euro 2020
season_id = 43 # 2021/22

# Define parser to extract match data
parser = Sbopen()

# Use API IDs to extract match ids
df_match = parser.match(competition_id=comp_id,season_id=season_id)
# Filter for the final
final_matchid = df_match.loc[df_match.competition_stage_name == 'Final'][['match_id']].values[0]
# Extract event data for the final
final_events, df_related, df_freeze, df_tactics = parser.event(final_matchid[0])

# Analysis on 2x midfielders for italy and 2x midfielders for England
verratti = final_events.loc[final_events.player_name == 'Marco Verratti']
jorginho = final_events.loc[final_events.player_name == 'Jorge Luiz Frello Filho']
rice = final_events.loc[final_events.player_name == 'Declan Rice']
mount = final_events.loc[final_events.player_name == 'Mason Mount']

# Filter for attacking events
verratti_attack = verratti.copy().loc[(verratti.type_name == 'Ball Receipt') | (verratti.type_name == 'Pass') | (verratti.type_name == 'Carry') | (verratti.type_name == 'Shot') | (verratti.type_name == 'Foul Won')].reset_index(drop=True)
jorginho_attack = jorginho.copy().loc[(jorginho.type_name == 'Ball Receipt') | (jorginho.type_name == 'Pass') | (jorginho.type_name == 'Carry') | (jorginho.type_name == 'Shot') | (jorginho.type_name == 'Foul Won')].reset_index(drop=True)
rice_attack = rice.copy().loc[(rice.type_name == 'Ball Receipt') | (rice.type_name == 'Pass') | (rice.type_name == 'Carry') | (rice.type_name == 'Shot') | (rice.type_name == 'Foul Won') | (rice.type_name == 'Dribble')].reset_index(drop=True)
mount_attack = mount.copy().loc[(mount.type_name == 'Ball Receipt') | (mount.type_name == 'Pass') | (mount.type_name == 'Carry') | (mount.type_name == 'Shot') | (mount.type_name == 'Foul Won') | (mount.type_name == 'Dribble')].reset_index(drop=True)

# Filter for defensive events
verratti_def = verratti.copy().loc[(verratti.type_name == 'Pressure') | (verratti.type_name == 'Foul Committed') | (verratti.type_name == 'Ball Recovery') | (verratti.type_name == 'Block') | (verratti.type_name == 'Interception') | (verratti.type_name == 'Dribbled Past')].reset_index(drop=True)
jorginho_def = jorginho.copy().loc[(jorginho.type_name == 'Pressure') | (jorginho.type_name == 'Foul Committed') | (jorginho.type_name == 'Ball Recovery') | (jorginho.type_name == 'Block') | (jorginho.type_name == 'Interception') | (jorginho.type_name == 'Dribbled Past') | (jorginho.type_name == 'Clearance')].reset_index(drop=True)
rice_def = rice.copy().loc[(rice.type_name == 'Pressure') | (rice.type_name == 'Foul Committed') | (rice.type_name == 'Ball Recovery') | (rice.type_name == 'Block') | (rice.type_name == 'Interception') | (rice.type_name == 'Dribbled Past') | (rice.type_name == 'Clearance')].reset_index(drop=True)
mount_def = mount.copy().loc[(mount.type_name == 'Pressure') | (mount.type_name == 'Foul Committed') | (mount.type_name == 'Ball Recovery') | (mount.type_name == 'Block') | (mount.type_name == 'Interception') | (mount.type_name == 'Dribbled Past') | (mount.type_name == 'Clearance')].reset_index(drop=True)

# Filter for complete and incomplete passes
verratti_passes = verratti_attack.loc[(verratti_attack.type_name == 'Pass') & (verratti_attack.outcome_name.isna())].reset_index(drop=True)
jorginho_passes = jorginho_attack.loc[(jorginho_attack.type_name == 'Pass') & (jorginho_attack.outcome_name.isna())].reset_index(drop=True)
rice_passes = rice_attack.loc[(rice_attack.type_name == 'Pass') & (rice_attack.outcome_name.isna())].reset_index(drop=True)
mount_passes = mount_attack.loc[(mount_attack.type_name == 'Pass') & (mount_attack.outcome_name.isna())].reset_index(drop=True)
verratti_passes_fail = verratti_attack.loc[(verratti_attack.type_name == 'Pass') & (verratti_attack.outcome_name.notnull())].reset_index(drop=True)
jorginho_passes_fail = jorginho_attack.loc[(jorginho_attack.type_name == 'Pass') & (jorginho_attack.outcome_name.notnull())].reset_index(drop=True)
rice_passes_fail = rice_attack.loc[(rice_attack.type_name == 'Pass') & (rice_attack.outcome_name.notnull())].reset_index(drop=True)
mount_passes_fail = mount_attack.loc[(mount_attack.type_name == 'Pass') & (mount_attack.outcome_name.notnull())].reset_index(drop=True)

### Verratti plots ###
# Plot the pitches for each player
pitch = VerticalPitch(pitch_type='statsbomb',pitch_color='#1E4966',line_color = '#c7d5cc',)
fig, axs = pitch.grid(ncols=3,axis=False)
fig.set_facecolor('#1E4966')
# Plot completed and incomplete passes
pitch.arrows(verratti_passes.x, verratti_passes.y, verratti_passes.end_x, verratti_passes.end_y, width=2, headwidth=5, headlength=5, color='aquamarine', label='Completed', ax=axs['pitch'][0])
pitch.arrows(verratti_passes_fail.x, verratti_passes_fail.y, verratti_passes_fail.end_x, verratti_passes_fail.end_y, width=2, headwidth=5, headlength=5, color='slategrey', label='Incomplete', ax=axs['pitch'][0])
axs['pitch'][0].legend(bbox_to_anchor=(0.062, 0.044))
axs['title'].text(0.11,-0.05,'Pass Map', fontsize = 20, color='white')

# Plot defensive actions
pitch.scatter(verratti_def.loc[verratti_def.type_name == 'Ball Recovery'].x,verratti_def.loc[verratti_def.type_name == 'Ball Recovery'].y,s=150,c='aquamarine',marker='*',label='Ball Recovery',ax=axs['pitch'][1])
pitch.scatter(verratti_def.loc[verratti_def.type_name == 'Block'].x,verratti_def.loc[verratti_def.type_name == 'Block'].y,s=125,marker='o',c='aquamarine',label='Block',ax=axs['pitch'][1])
pitch.scatter(verratti_def.loc[verratti_def.type_name == 'Interception'].x,verratti_def.loc[verratti_def.type_name == 'Interception'].y,s=100,marker='d',c='aquamarine',label='Interception',ax=axs['pitch'][1])
pitch.scatter(verratti_def.loc[verratti_def.type_name == 'Dribbled Past'].x,verratti_def.loc[verratti_def.type_name == 'Dribbled Past'].y,s=100,marker='p',c='slategrey',label='Dribbled Past',ax=axs['pitch'][1])
pitch.scatter(verratti_def.loc[verratti_def.type_name == 'Foul Committed'].x,verratti_def.loc[verratti_def.type_name == 'Foul Committed'].y,s=150,c='slategrey',marker='x',label='Foul',ax=axs['pitch'][1])
axs['pitch'][1].legend(bbox_to_anchor=(0.38, 0.043))
axs['title'].text(0.419,-0.05,'Defensive Actions', fontsize = 20, color='white')

# Plot pressure heatmap
pitch.kdeplot(verratti_def.loc[verratti_def.type_name == 'Pressure'].x,verratti_def.loc[verratti_def.type_name == 'Pressure'].y,cut=5,alpha=0.75,ax=axs['pitch'][2],color='aquamarine',fill=True)
axs['title'].text(0.76,-0.05,'Pressures Heatmap', fontsize = 20, color='white')

axs['title'].text(0.225,0.7,'Euro 2020 Final: Central Midfield Analysis',fontsize=25,color='white',weight='bold')
axs['title'].text(0.405,0.35,'Marco Verratti',fontsize=25,color='white',weight='bold')

axs['endnote'].text(0.9025,0.825,'Twitter: @datawithed',color='white',fontsize=10)
axs['endnote'].text(0.8751,0.575,'Instagram: @data_with_ed',color='white',fontsize=10)
axs['endnote'].text(0.8945,1.1,'Data via: StatsBomb',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,1.1,'Passing:',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,0.825,'Complete: 103.0 (92.79%)',color='white',fontsize=10)
axs['endnote'].text(0,0.575,'Incomplete: 8.0 (7.21%)',color='white',fontsize=10)
axs['endnote'].text(0.41,0.7,'Manager: Roberto Mancini',color='white',fontsize=15)
axs['endnote'].text(0.44,0.3,'Formation: 4-3-3',color='white',fontsize=15)
plt.savefig('Euro 2020 MF analysis - Verratti.png')


### Jorginho plots ###
# Plot the pitches for each player
pitch = VerticalPitch(pitch_type='statsbomb',pitch_color='#1E4966',line_color = '#c7d5cc',)
fig, axs = pitch.grid(ncols=3,axis=False)
fig.set_facecolor('#1E4966')
# Plot completed and incomplete passes
pitch.arrows(jorginho_passes.x, jorginho_passes.y, jorginho_passes.end_x, jorginho_passes.end_y, width=2, headwidth=5, headlength=5, color='aquamarine', label='Completed', ax=axs['pitch'][0])
pitch.arrows(jorginho_passes_fail.x, jorginho_passes_fail.y, jorginho_passes_fail.end_x, jorginho_passes_fail.end_y, width=2, headwidth=5, headlength=5, color='slategrey', label='Incomplete', ax=axs['pitch'][0])
axs['pitch'][0].legend(bbox_to_anchor=(0.062, 0.044))
axs['title'].text(0.11,-0.05,'Pass Map', fontsize = 20, color='white')

# Plot defensive actions
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Ball Recovery'].x,jorginho_def.loc[jorginho_def.type_name == 'Ball Recovery'].y,s=150,c='aquamarine',marker='*',label='Ball Recovery',ax=axs['pitch'][1])
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Block'].x,jorginho_def.loc[jorginho_def.type_name == 'Block'].y,s=125,marker='o',c='aquamarine',label='Block',ax=axs['pitch'][1])
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Interception'].x,jorginho_def.loc[jorginho_def.type_name == 'Interception'].y,s=100,marker='d',c='aquamarine',label='Interception',ax=axs['pitch'][1])
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Clearance'].x,jorginho_def.loc[jorginho_def.type_name == 'Clearance'].y,s=100,c='slategrey',marker='s',label='Clearance',ax=axs['pitch'][1])
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Dribbled Past'].x,jorginho_def.loc[jorginho_def.type_name == 'Dribbled Past'].y,s=100,marker='p',c='slategrey',label='Dribbled Past',ax=axs['pitch'][1])
pitch.scatter(jorginho_def.loc[jorginho_def.type_name == 'Foul Committed'].x,jorginho_def.loc[jorginho_def.type_name == 'Foul Committed'].y,s=150,c='slategrey',marker='x',label='Foul',ax=axs['pitch'][1])
axs['pitch'][1].legend(bbox_to_anchor=(0.32, 0.0425),prop={'size':8})
axs['title'].text(0.419,-0.05,'Defensive Actions', fontsize = 20, color='white')

# Plot pressure heatmap
pitch.kdeplot(jorginho_def.loc[jorginho_def.type_name == 'Pressure'].x,jorginho_def.loc[jorginho_def.type_name == 'Pressure'].y,cut=5,alpha=0.75,ax=axs['pitch'][2],color='aquamarine',fill=True)
axs['title'].text(0.76,-0.05,'Pressures Heatmap', fontsize = 20, color='white')

axs['title'].text(0.225,0.7,'Euro 2020 Final: Central Midfield Analysis',fontsize=25,color='white',weight='bold')
axs['title'].text(0.425,0.35,'Jorginho',fontsize=25,color='white',weight='bold')

axs['endnote'].text(0.9025,0.825,'Twitter: @datawithed',color='white',fontsize=10)
axs['endnote'].text(0.8751,0.575,'Instagram: @data_with_ed',color='white',fontsize=10)
axs['endnote'].text(0.8945,1.1,'Data via: StatsBomb',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,1.1,'Passing:',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,0.825,'Complete: 90.0 (93.75%)',color='white',fontsize=10)
axs['endnote'].text(0,0.575,'Incomplete: 6.0 (6.25%)',color='white',fontsize=10)
axs['endnote'].text(0.41,0.7,'Manager: Roberto Mancini',color='white',fontsize=15)
axs['endnote'].text(0.44,0.3,'Formation: 4-3-3',color='white',fontsize=15)
plt.savefig('Euro 2020 MF analysis - Jorginho.png')

### Mount plots ###
# Plot the pitches for each player
pitch = VerticalPitch(pitch_type='statsbomb',pitch_color='#1E4966',line_color = '#c7d5cc',)
fig, axs = pitch.grid(ncols=3,axis=False)
fig.set_facecolor('#1E4966')
# Plot completed and incomplete passes
pitch.arrows(mount_passes.x, mount_passes.y, mount_passes.end_x, mount_passes.end_y, width=2, headwidth=5, headlength=5, color='aquamarine', label='Completed', ax=axs['pitch'][0])
pitch.arrows(mount_passes_fail.x, mount_passes_fail.y, mount_passes_fail.end_x, mount_passes_fail.end_y, width=2, headwidth=5, headlength=5, color='slategrey', label='Incomplete', ax=axs['pitch'][0])
axs['pitch'][0].legend(bbox_to_anchor=(0.062, 0.044))
axs['title'].text(0.11,-0.05,'Pass Map', fontsize = 20, color='white')

# Plot defensive actions
pitch.scatter(mount_def.loc[mount_def.type_name == 'Ball Recovery'].x,mount_def.loc[mount_def.type_name == 'Ball Recovery'].y,s=150,c='aquamarine',marker='*',label='Ball Recovery',ax=axs['pitch'][1])
pitch.scatter(mount_def.loc[mount_def.type_name == 'Block'].x,mount_def.loc[mount_def.type_name == 'Block'].y,s=125,marker='o',c='aquamarine',label='Block',ax=axs['pitch'][1])
pitch.scatter(mount_def.loc[mount_def.type_name == 'Dribbled Past'].x,mount_def.loc[mount_def.type_name == 'Dribbled Past'].y,s=100,marker='p',c='slategrey',label='Dribbled Past',ax=axs['pitch'][1])
pitch.scatter(mount_def.loc[mount_def.type_name == 'Foul Committed'].x,mount_def.loc[mount_def.type_name == 'Foul Committed'].y,s=150,c='slategrey',marker='x',label='Foul',ax=axs['pitch'][1])
axs['pitch'][1].legend(bbox_to_anchor=(0.385, 0.0425),prop={'size':10})
axs['title'].text(0.419,-0.05,'Defensive Actions', fontsize = 20, color='white')

# Plot pressure heatmap
pitch.kdeplot(mount_def.loc[mount_def.type_name == 'Pressure'].x,mount_def.loc[mount_def.type_name == 'Pressure'].y,cut=5,alpha=0.75,ax=axs['pitch'][2],color='aquamarine',fill=True)
axs['title'].text(0.76,-0.05,'Pressures Heatmap', fontsize = 20, color='white')

axs['title'].text(0.225,0.7,'Euro 2020 Final: Central Midfield Analysis',fontsize=25,color='white',weight='bold')
axs['title'].text(0.41,0.35,'Mason Mount',fontsize=25,color='white',weight='bold')

axs['endnote'].text(0.9025,0.825,'Twitter: @datawithed',color='white',fontsize=10)
axs['endnote'].text(0.8751,0.575,'Instagram: @data_with_ed',color='white',fontsize=10)
axs['endnote'].text(0.8945,1.1,'Data via: StatsBomb',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,1.1,'Passing:',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,0.825,'Complete: 14.0 (63.64%)',color='white',fontsize=10)
axs['endnote'].text(0,0.575,'Incomplete: 8.0 (36.36%)',color='white',fontsize=10)
axs['endnote'].text(0.405,0.7,'Manager: Gareth Southgate',color='white',fontsize=15)
axs['endnote'].text(0.43,0.3,'Formation: 3-4-2-1',color='white',fontsize=15)
plt.savefig('Euro 2020 MF analysis - Mount.png')


### Rice plots ###
# Plot the pitches for each player
pitch = VerticalPitch(pitch_type='statsbomb',pitch_color='#1E4966',line_color = '#c7d5cc',)
fig, axs = pitch.grid(ncols=3,axis=False)
fig.set_facecolor('#1E4966')
# Plot completed and incomplete passes
pitch.arrows(rice_passes.x, rice_passes.y, rice_passes.end_x, rice_passes.end_y, width=2, headwidth=5, headlength=5, color='aquamarine', label='Completed', ax=axs['pitch'][0])
pitch.arrows(rice_passes_fail.x, rice_passes_fail.y, rice_passes_fail.end_x, rice_passes_fail.end_y, width=2, headwidth=5, headlength=5, color='slategrey', label='Incomplete', ax=axs['pitch'][0])
axs['pitch'][0].legend(bbox_to_anchor=(0.062, 0.044))
axs['title'].text(0.11,-0.05,'Pass Map', fontsize = 20, color='white')

# Plot defensive actions
pitch.scatter(rice_def.loc[rice_def.type_name == 'Ball Recovery'].x,rice_def.loc[rice_def.type_name == 'Ball Recovery'].y,s=150,c='aquamarine',marker='*',label='Ball Recovery',ax=axs['pitch'][1])
pitch.scatter(rice_def.loc[rice_def.type_name == 'Block'].x,rice_def.loc[rice_def.type_name == 'Block'].y,s=125,marker='o',c='aquamarine',label='Block',ax=axs['pitch'][1])
pitch.scatter(rice_def.loc[rice_def.type_name == 'Interception'].x,rice_def.loc[rice_def.type_name == 'Interception'].y,s=100,marker='d',c='aquamarine',label='Interception',ax=axs['pitch'][1])
pitch.scatter(rice_def.loc[rice_def.type_name == 'Clearance'].x,rice_def.loc[rice_def.type_name == 'Clearance'].y,s=100,c='slategrey',marker='s',label='Clearance',ax=axs['pitch'][1])
pitch.scatter(rice_def.loc[rice_def.type_name == 'Dribbled Past'].x,rice_def.loc[rice_def.type_name == 'Dribbled Past'].y,s=100,marker='p',c='slategrey',label='Dribbled Past',ax=axs['pitch'][1])
pitch.scatter(rice_def.loc[rice_def.type_name == 'Foul Committed'].x,rice_def.loc[rice_def.type_name == 'Foul Committed'].y,s=150,c='slategrey',marker='x',label='Foul',ax=axs['pitch'][1])
axs['pitch'][1].legend(bbox_to_anchor=(0.625, 0.05),prop={'size':10})
axs['title'].text(0.419,-0.05,'Defensive Actions', fontsize = 20, color='white')

# Plot pressure heatmap
pitch.kdeplot(rice_def.loc[rice_def.type_name == 'Pressure'].x,rice_def.loc[rice_def.type_name == 'Pressure'].y,cut=5,alpha=0.75,ax=axs['pitch'][2],color='aquamarine',fill=True)
axs['title'].text(0.76,-0.05,'Pressures Heatmap', fontsize = 20, color='white')

axs['title'].text(0.225,0.7,'Euro 2020 Final: Central Midfield Analysis',fontsize=25,color='white',weight='bold')
axs['title'].text(0.42,0.35,'Declan Rice',fontsize=25,color='white',weight='bold')

axs['endnote'].text(0.9025,0.825,'Twitter: @datawithed',color='white',fontsize=10)
axs['endnote'].text(0.8751,0.575,'Instagram: @data_with_ed',color='white',fontsize=10)
axs['endnote'].text(0.8945,1.1,'Data via: StatsBomb',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,1.1,'Passing:',color='white',fontsize=10,weight='bold')
axs['endnote'].text(0,0.825,'Complete: 25.0 (86.21%)',color='white',fontsize=10)
axs['endnote'].text(0,0.575,'Incomplete: 4.0 (13.79%)',color='white',fontsize=10)
axs['endnote'].text(0.405,0.7,'Manager: Gareth Southgate',color='white',fontsize=15)
axs['endnote'].text(0.43,0.3,'Formation: 3-4-2-1',color='white',fontsize=15)
plt.savefig('Euro 2020 MF analysis - Rice.png')


