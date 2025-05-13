import { ActionRowBuilder, ButtonBuilder, ButtonStyle, ComponentType, StringSelectMenuBuilder, StringSelectMenuOptionBuilder,
    GuildMember,  TextChannel } from "discord.js";

let grades = {"12":"1371047485635694633", "11":"1371388371280199740"}
let secL = {"12A":"1371387449326047275", "12B":"1371387563356721183", "12C":"1370063304650788894", "12D":"1370063558796120154", "12E":"1371852477821096068","12F":"1371388270289616906",
            "11A":"1371388413323771916", "11B":"1371388451806642239", "11C":"1371388492869013565", "11D":"1371388525328470077", "11E":"1371388554063904788","11F":"1371388593225994241"
}
export const onMemberJoin = async (guy: GuildMember) => {
    console.log("Member joined")
    if (guy.guild.id == "1370062593603010621") {
        guy.roles.add("1370073421504839690");
        const ch = await guy.guild.channels.fetch("1370072981656571995") as TextChannel
        const m = await ch.send({
            content:`Hello there <@${guy.id}>! Please wait for <@602098932260143124> to verify you.\nMeanwhile read <#1370074384005333042> choose your class and section roles then talk`,
            components:[classes]
        })
        let collector = m.createMessageComponentCollector({componentType:ComponentType.StringSelect, time:10*60*1000, filter:i => i.user.id == guy.id});
        let c:string;
        collector.on("collect", async i => {
            if (i.customId == "class") {
                c = i.values[0]
                await i.update({content:`You have selected class ${c}`, components:[ new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(StringSelectMenuBuilder.from((i.component)).setDisabled(true)), sections]})
                guy.roles.add(grades[c as keyof typeof grades])
            }
            else if (i.customId == "section") {
                const s = i.values[0]
                guy.roles.add(secL[c+s as keyof typeof secL])
            }

        })
    }
    if (guy.guild.id == "784754833319919647") {
        guy.roles.add("799023357587881985")
        const c = await guy.guild.channels.fetch("784754833869242440") as TextChannel
        const m = c.send(`Hello there <@${guy.id}>! Please wait for mods to add your roles`)
    }
};
const classes = new ActionRowBuilder<StringSelectMenuBuilder>()
    .addComponents(
        new StringSelectMenuBuilder()
            .setCustomId("class")
            .addOptions(
                [12,11,10].map(c => 
                    new StringSelectMenuOptionBuilder()
                        .setLabel(`${c}th`)
                        .setDescription(`${c}th class`)
                        .setValue(`${c}`)
                )
            )
    )
const sections = new ActionRowBuilder<StringSelectMenuBuilder>()
    .addComponents(
        new StringSelectMenuBuilder()
            .setCustomId("section")
            .addOptions(
                ["A", "B", "C", "D", "E", "F"].map(s => 
                new StringSelectMenuOptionBuilder()
                    .setLabel(s)
                    .setDescription(`Section {s}`)
                    .setValue(s)
                )
            )
    )
/*
const c12 = new ButtonBuilder()
    .setCustomId("12")
    .setLabel("12th")
    .setStyle(ButtonStyle.Primary)
const c11 = new ButtonBuilder()
    .setCustomId("11")
    .setLabel("11th")
    .setStyle(ButtonStyle.Primary)
const c10 = new ButtonBuilder()
    .setCustomId("10")
    .setLabel("10th")
    .setStyle(ButtonStyle.Primary)

const classes =  new ActionRowBuilder<ButtonBuilder>()
    .addComponents([c12, c11, c10])

const sA = new ButtonBuilder()
    .setCustomId("seca")
    .setLabel("A")
const sB = new ButtonBuilder()
    .setCustomId("secb")
    .setLabel("B")
const sC = new ButtonBuilder()
    .setCustomId("secc")
    .setLabel("C")
const sD = new ButtonBuilder()
    .setCustomId("secd")
    .setLabel("D")
const sE = new ButtonBuilder()
    .setCustomId("sece")
    .setLabel("E")
const sF = new ButtonBuilder()
    .setCustomId("secf")
    .setLabel("F")

const sections = new ActionRowBuilder<ButtonBuilder>()
    .addComponents(sA,sB,sC,sD,sE,sF)
*/