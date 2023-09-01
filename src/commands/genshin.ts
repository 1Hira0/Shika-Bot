import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { EmbedBuilder, SlashCommandBuilder } from 'discord.js';

export const showcase: Command = {
    data:new SlashCommandBuilder()
            .setName('showcase')
            .setDescription("Showcase an account and characters")
            .addIntegerOption(options => 
                options.setName('uid')
                       .setDescription("UID of the account(will add UID setups for accounts later)")
                       .setRequired(true)
                       .setMaxValue(999999999)
                       .setMinValue(100000000)),
    run:async (interaction) => {
        await interaction.deferReply();
        const response = await fetch(`https://enka.network/api/u/${interaction.options.get('uid')?.value}?info`)
        console.log(response)
        if (response.status != 200) {
            await interaction.editReply(`Some error occurred: ${response.status}`) //to add error handling
            return;
        }
        const data = await response.json()
        const playerInfo = data.playerInfo;
        const char = playerInfo.showAvatarInfoList
        let dex = ''
        for(let i=0;i<8;i++) {
            dex = `${dex}${char[i].avatarId}: ${char[i].level}\n`
        }

        const embed = new EmbedBuilder()
                            .setTitle(playerInfo.nickname)
                            .setURL(`https://enka.network/uid/${data.uid}`)
                            .setDescription(dex);
        await interaction.editReply({embeds:[embed]});
    }
}