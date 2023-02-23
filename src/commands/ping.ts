import { Command } from "../interfaces/Command"
import { SlashCommandBuilder } from 'discord.js';

export const ping: Command = {
    data: new SlashCommandBuilder()
        .setName("jsping")
        .setDescription("sends latency of client"),
    run: async (interaction) => {
            let starttime = (Number(interaction.id) >> 2) + 1420070400000;
            await interaction.reply({content:'Checking ping! :ping_pong:', fetchReply:true});
            const message = await interaction.fetchReply();
            let endtime = (Number(message.id) >> 2) + 1420070400000;
            await interaction.editReply({content:`Websocket: ${Math.round(interaction.client.ws.ping)}ms || RoundABout:${endtime-starttime}ms`})
    }
};