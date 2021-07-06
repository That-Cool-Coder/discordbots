import { Chatbot } from './standaloneChatbot.mjs';


var name = process.argv[2];
var input = process.argv.slice(3).join(' ');
var chatbot = new Chatbot(name);
console.log(chatbot.processSentence(input));