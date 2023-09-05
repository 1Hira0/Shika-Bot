import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { EmbedBuilder, SlashCommandBuilder } from 'discord.js';
import fs from 'fs';

const charDetails = JSON.parse(fs.readFileSync('E:\\Hira\\data\\characters.json', 'utf-8')); //src: https://github.com/EnkaNetwork/API-docs/blob/master/store/characters.json
const charHash = JSON.parse(fs.readFileSync('E:\\Hira\\data\\TextMapEN.json', 'utf-8'));     //src: https://gitlab.com/Dimbreath/AnimeGameData/-/blob/master/TextMap/TextMapEN.json

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
        const response = await fetch(`https://enka.network/api/uid/${interaction.options.get('uid')?.value}?info`)
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
            dex = `${dex}${charHash[charDetails[char[i].avatarId].NameTextMapHash]}: ${char[i].level}\n`
        }

        const embed = new EmbedBuilder()
                            .setTitle(playerInfo.nickname)
                            .setURL(`https://enka.network/u/${data.uid}`)
                            .setDescription(dex);
        await interaction.editReply({embeds:[embed]});
    }
}