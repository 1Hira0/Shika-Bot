import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { EmbedBuilder, SlashCommandBuilder } from 'discord.js';
import { getDominantColour } from '../extras';

const mal_icon = "https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAiC8a86sHufn_jOI-JGtoCQ"
const anilist_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/AniList_logo.svg/2048px-AniList_logo.svg.png"

export const jsanime: Command = {
    data: new SlashCommandBuilder()
        .setName("jsanime")
        .setDescription("Anime info")
        .addStringOption(option =>
            option.setName('anime')
                    .setDescription("Name of the anime")
                    .setRequired(true)),
    run: async (interaction) =>{
        await interaction.deferReply()
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
								siteUrl
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
        const r = await response.json();
		if (r.data.Page.media.length && Array.isArray(r.data.Page.media)) {
			const anime = r.data.Page.media[0]
			let dex = anime.description
			if (dex.length > 4096) {
				dex = dex.slice(4090) + "`...`"
			}
        	const emb = new EmbedBuilder()
        	        .setDescription(dex.replace(/<(i|\/i|br)>/gm, "").replace(/(~!|!~)/gm, "||"))
        	        .setTitle(anime.title.romaji)
        	        .setURL(anime.siteUrl)
					.setAuthor({name:"Don't like AL? Try MAL by clicking here", url:`https://mynaimelist.net/anime/${anime.idMal}`, iconURL:mal_icon})
					.setColor(anime.coverImage.color)
					.setImage(`https://img.anili.st/media/${anime.id}`)
					.setThumbnail(anime.coverImage.extraLarge)
					.setFooter({text:"Get more information at Anilist by clicking the blue text at top"})
        	await interaction.editReply({embeds:[emb]})
        } else {
			await interaction.editReply({content:`No entry found with title "${interaction.options.get("anime")?.value}". Please try again after checking the spelling and typos.`})
		}
    }
};

export const jschar: Command = {
	data: new SlashCommandBuilder()
		.setName("jscharacter")
		.setDescription("Character info")
		.addStringOption(option=>
			option.setName('name')
				  .setDescription('Name of the character')
				  .setRequired(true)),
	run: async (interaction) => {
		await interaction.deferReply()
		const response = await fetch('https://graphql.anilist.co',{
          	method: 'POST',
          	headers: {
          	    'Content-Type': 'application/json',
          	    'Accept': 'application/json',
          	},
          	body: JSON.stringify({
          	    query: `query ($id: Int, $page: Int, $perPage: Int, $search: String) {
					Page (page: $page, perPage: $perPage) {
					  	pageInfo {
							total
							currentPage
							lastPage
							hasNextPage
							perPage
					  	}
					  	characters (id: $id, search: $search) {
							id
							siteUrl
							image {
								large
							}
							name {
						  		userPreferred
							}
						  	description(asHtml:false)
					  	}
					}
				}`,
          	    variables: { "search":interaction.options.get("name")?.value, "page":1, "perPage":1}
          	})
      	});
		const res = await response.json()
		if (res.data.Page.characters.length && Array.isArray(res.data.Page.characters)) {
			const character = res.data.Page.characters[0];
			console.log(character)
			let dex:string
			if (character.description.length) {
				dex = `${character.description}`.replace(/<a href="(?<link>.+?)">(\s*)?(?<name>.+?)(\s*)?<\/a>/gm, "")
			} else {
				dex = " "
			}
			if (dex.length > 4096) {
				dex = dex.slice(4090) + "`...`"
			}
			const emb = new EmbedBuilder()
				.setTitle(character.name.userPreferred)
				.setDescription(dex.replace(/<(i|\/i|br)>/gm, "").replace(/(~![\d\w]+?!~)/gm, "||"))
				.setURL(character.siteUrl)
				.setAuthor({name:`Anilist`,iconURL:anilist_icon, url:`https://anilist.co`})// (no ids for characters) 
				.setColor(await getDominantColour(character.image.large))
				.setImage(character.image.large)
				.setFooter({text:`For more details click the BIG BLue Link to go to Anilist`})
			await interaction.editReply({embeds:[emb]})
		} else {
			await interaction.editReply(`No character found with name "${interaction.options.get("name")?.value}". Please try again after checking spelling and typos`)
		}
	}
};

export const jsmanga: Command = {
	data: new SlashCommandBuilder()
		.setName("jsmanga")
		.setDescription("Sends manga info with js"),
	run: async (interaction) => {
		await interaction.reply({content:"Command in development"})
	}
};

export const jsstudio: Command = {
	data: new SlashCommandBuilder()
		.setName("jsstudio")
		.setDescription("Sends studio info with js"),
	run: async (interaction) => {
		await interaction.reply({content:"Command in development"})
	}
};