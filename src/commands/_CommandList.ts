import { Command } from "../interfaces/Command";
import { ping } from "./ping"
import { jsanime, jsstudio, jschar, jsmanga } from "./anime";

export const CommandList: Command[] = [/*ping,*/ jsanime, jsstudio, jschar, jsmanga];