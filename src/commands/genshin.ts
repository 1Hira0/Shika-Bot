import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { ActionRowBuilder, ComponentType, EmbedBuilder, SlashCommandBuilder, StringSelectMenuBuilder, StringSelectMenuOptionBuilder } from 'discord.js';
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
        const msg = await interaction.deferReply();
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
        let options = []
        for(let i=0;i<8;i++) {
            dex = `${dex}${charHash[charDetails[char[i].avatarId].NameTextMapHash]}: ${char[i].level}\n`
            options.push(new StringSelectMenuOptionBuilder()
                            .setLabel(charHash[charDetails[char[i].avatarId].NameTextMapHash])
                            .setValue(`${char[i].avatarId}`))
        };

        const embed = new EmbedBuilder()
                            .setTitle(playerInfo.nickname)
                            .setURL(`https://enka.network/u/${data.uid}`)
                            .setDescription(dex);
        const select = new StringSelectMenuBuilder()
            .setCustomId('mommy')
            .setPlaceholder('Show character')
            .addOptions(options);
        const row = new ActionRowBuilder<StringSelectMenuBuilder>()
            .addComponents(select);
        await interaction.editReply({embeds:[embed], components:[row]});
        
        const collector = msg.createMessageComponentCollector({componentType:ComponentType.StringSelect, time:(15*60)*1000})
 
    }
}