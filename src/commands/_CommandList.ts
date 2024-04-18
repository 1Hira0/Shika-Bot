import { Command } from "../interfaces/Command";
import { ping } from "./ping"
import { anime, studio, char, manga } from "./anime";
import { showcase } from './genshin';

export const CommandList: Command[] = [/*ping,*/ anime, studio, char, manga, showcase];