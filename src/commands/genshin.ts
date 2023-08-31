import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { EmbedBuilder, SlashCommandBuilder } from 'discord.js';

export const showcase: Command = {
    data:new SlashCommandBuilder,
    run:async (interaction) => {
        await interaction.reply("Command in development");
    }
}