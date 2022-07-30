import fetch from 'node-fetch';
import { Command } from "../interfaces/Command"
import { SlashCommandBuilder } from "@discordjs/builders";
import { EmbedBuilder, EmbedAuthorOptions } from 'discord.js';

export const jsanime: Command = {
    data: new SlashCommandBuilder()
        .setName("jsanime")
        .setDescription("sends anime with js")
        .addStringOption(option =>
            option.setName('anime')
                    .setDescription("Name of the anime")
                    .setRequired(true)),
    run: async (interaction) =>{
        //await interaction.deferReply()
        const response = await fetch('https://graphql.anilist.co',{
          	method: 'POST',
          	headers: {
          	    'Content-Type': 'application/json',
          	    'Accept': 'application/json',
          	},
          	body: JSON.stringify({
          	    query: `
					query ($id: Int, $page: Int, $perPage: Int, $search: String) {
  						Page (page: $page, perPage: $perPage) {
    						pageInfo {
      							total
      							currentPage
      							lastPage
      							hasNextPage
      							perPage
    						}
    						media (id: $id, search: $search, type:ANIME) {
      							id
								idMal
      							title {
        						english
								romaji
      							}
								description
								bannerImage
								coverImage {
									color
									extraLarge
								}
    						}
  						}
					}
				`,
          	    variables: { "search":interaction.options.get("anime")?.value, "page":1, "perPage":1}
          	})
      	});
        const data = await response.json();
		console.log(data);
		console.log(data.data);
		console.log(data.data.Page.media);
        const emb = new EmbedBuilder()
                .setDescription(data.data.Page.media[0].description.replaceAll("<i>", "").replaceAll("</i>", "").replaceAll("<br>", ""))
                .setTitle(data.data.Page.media[0].title.romaji)
                .setURL(`https://anilist.co/${data.data.Page.media[0].id}/${data.data.Page.media[0].title.romaji.replace(' ', "-")}`)
				.setAuthor({name:"Tap here to play", url:`https://animixplay.to/anime/${data.data.Page.media[0].idMal}`, iconURL:"https://animixplay.to/icon.png"})
				.setColor(data.data.Page.media[0].coverImage.color)
				.setImage(`https://img.anili.st/media/${data.data.Page.media[0].id}`)
				.setThumbnail(data.data.Page.media[0].coverImage.bannerImage)
        await interaction.reply({embeds:[emb]})
        
        }
};
export const jschar: Command = {
	data: new SlashCommandBuilder()
		.setName("jscharacter")
		.setDescription("Sends character info with js"),
	run: async (interaction) => {
		await interaction.reply({content:"Command in development"})
	}
}
export const jsmanga: Command = {
	data: new SlashCommandBuilder()
		.setName("jsmanga")
		.setDescription("Sends manga info with js"),
	run: async (interaction) => {
		await interaction.reply({content:"Command in development"})
	}
}
export const jsstudio: Command = {
	data: new SlashCommandBuilder()
		.setName("jsstudio")
		.setDescription("Sends studio info with js"),
	run: async (interaction) => {
		await interaction.reply({content:"Command in development"})
	}
}