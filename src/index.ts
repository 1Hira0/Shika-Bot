import { ActivityType, Client, GatewayIntentBits } from "discord.js";
import { onInteraction } from "./events/onInteraction";
import { onReady } from "./events/onReady";
import { onMemberJoin } from "./events/memberJoin";

console.log("Running");
(async () => {
    const bot = new Client({
        intents: [
            GatewayIntentBits.Guilds,
            GatewayIntentBits.GuildMessages,
            GatewayIntentBits.MessageContent
        ]
    });
    bot.on("ready", async () => {
        await onReady(bot); 
        bot.user?.setPresence({ 
            activities: [{ 
                type:ActivityType.Playing , 
                name: 'My father will never complete me' 
            }], 
            status: 'idle' 
        });
    });
        
    bot.on("interactionCreate", async (interaction) => await onInteraction(interaction));
    bot.on("guildMemberAdd", async (i) => await onMemberJoin(i))
    await bot.login(process.env.BOT_TOKEN);
})();