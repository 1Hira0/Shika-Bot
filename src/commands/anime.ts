import fetch from 'node-fetch';
import { Command } from "../interfaces/Command";
import { EmbedBuilder, SlashCommandBuilder } from 'discord.js';
import { getDominantColour } from '../extras';

const mal_icon = "https://image.myanimelist.net/ui/OK6W_koKDTOqqqLDbIoPAiC8a86sHufn_jOI-JGtoCQ"
const anilist_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/AniList_logo.svg/2048px-AniList_logo.svg.png"

export const jsanime: Command = {
    data: new SlashCommandBuilder()
        .setName("anime")
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
		.setName("character")
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
		.setName("manga")
		.setDescription("Manga info")
		.addStringOption(option => 
			option.setName("title")
				.setDescription("Title of the manga")
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
									media (id: $id, search: $search, type:MANGA) {
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
						  variables: { "search":interaction.options.get("title")?.value, "page":1, "perPage":1}
						})
		  });
		const r = await response.json();
		if (r.data.Page.media.length && Array.isArray(r.data.Page.media)) {
						const manga = r.data.Page.media[0]
						let dex = `${manga.description}`.replace(/<((\/|\\){0,1}?(i|br)(\/|\\){0,1}?)>/gm, "").replace(/(~!|!~)/gm, "||")
						if (dex.length > 4096) {
							dex = dex.slice(4090) + "`...`"
						}
						const emb = new EmbedBuilder()
								.setDescription(dex)
								.setTitle(manga.title.romaji)
								.setURL(manga.siteUrl)
								.setAuthor({name:"Don't like AL? Try MAL by clicking here", url:`https://mynanimelist.net/manga/${manga.idMal}`, iconURL:mal_icon})
								.setColor(manga.coverImage.color)
								.setImage(`https://img.anili.st/media/${manga.id}`)
								.setThumbnail(manga.coverImage.extraLarge)
								.setFooter({text:"Get more information at Anilist by clicking the blue text at top"})
						await interaction.editReply({embeds:[emb]})
		} else {
			await interaction.editReply({content:`No entry found with title "${interaction.options.get("title")?.value}". Please try again after checking the spelling and typos.`})
		}
	}
};

export const jsstudio: Command = {
	data: new SlashCommandBuilder()
		.setName("studio")
		.setDescription("studio info")
		.addStringOption(option=>
			option.setName("name")
				  .setDescription("Name of the studio")
				  .setRequired(true))
		.addNumberOption(option=>
			option.setName("id")
				  .setRequired(false)
				  .setDescription("ID of the studio. Required name won't be considered so enter gibbrish")),
	run: async (interaction) => {
		await interaction.deferReply()
		const response = await fetch("https://graphql.anilist.co", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Accept": "application/json"
			},
			body: JSON.stringify({
				query: `query ($id: Int $search: String) {
							Page (page: 1, perPage: 1) {
								pageInfo {
									  total
									  currentPage
									  lastPage
									  hasNextPage
									  perPage
								}
								studios (id:$id, search:$search, sort: [
									SEARCH_MATCH, SEARCH_MATCH, NAME, FAVOURITES
								]) {
									id
									name
									siteUrl
									media (sort:[POPULARITY,SCORE], perPage:10, page:1){
										nodes {siteUrl 
											   title {userPreferred}
										}
									}
								}
							} 
				}`, variables: interaction.options.get('id')? {"id": interaction.options.get('id')?.value}: {"search":interaction.options.get('name')?.value}
			})
		});
		const r = await response.json();
		if (!r.data.Page.studios) {
			await interaction.editReply({
				content:`No studio found with "${interaction.options.get(interaction.options.get('id')? "id":"name")?.value}".
				Please try again after checking the parameters provided.`});
			return}
		const stud = r.data.Page.studios[0];
		let dex = ''
		for (let i=0;i<stud.media.nodes.length-1;i++) {
			dex = `${dex}[${stud.media.nodes[i].title.userPreferred}](${stud.media.nodes[i].siteUrl})\n`
		}
		const emb = new EmbedBuilder()
			     .setTitle(stud.name)
				 .setDescription(dex)
				 .setURL(stud.siteUrl)
		await interaction.editReply({embeds:[emb]})
	}	 
};