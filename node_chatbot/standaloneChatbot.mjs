// Note that this version has been modified to run on node instead of in browser

// keywords
// --------

const userRelatedKeywords = ['me', 'i', 'my', 'mine'];
const selfRelatedKeywords = ['chatbox', 'you', 'you\'re', 'your', 'ravi'];
const objectRelatedKeywords = ['that', 'that\'s', 'the'];

const greetings = ['hi', 'hello', 'cheers', 'gday', 'g\'day', 'good morning', 'good day', 'good evening',
    'good afternoon', 'good night'];
const farewells = ['bye', 'goodbye', 'see you', 'see ya'];

const boolQuestionWords = [
    'did you', 'did we', 'did i', 'did he', 'did she', 'did his', 'did her', 'did your', 'did they', 'did it',
        'did that', 'did their', 'did its', 'did it\'s', 'did that',
    'has he', 'has she', 'have they', 'has it', 'has that', 'has his', 'has her', 'has their',
        'has its', 'has it\'s',
    'do you', 'does he', 'does she', 'does it', 'do they', 'does your', 'does his', 'does hers', 'does its',
        'does their', 'do i', 'did i',
    'are you', 'are they', 'are your', 'are their',
    'is he', 'is she', 'is it', 'is their', 'is his', 'is hers', 'is its', 'is your', 'am i',
    'should i', 'should he', 'should she', 'should it', 'should they', 'should you',
    'will you', 'will i', 'will he', 'will she', 'will it', 'will they'
];

const otherQuestionWords = [
    'what is', 'what are', 'what did', 'what\'s', 'what will',
    'who is', 'who are', 'who did', 'who\'s',
    'why is', 'why are', 'why did', 'why\'s', 'why do', 'why don\'t', 
        'why does', 'why doesn\'t', 'why will', 'why won\'t', 'why should', 'why shouldn\'t',
    'when is', 'when are', 'when did', 'when you', 'when he', 'when she', 'when they', 'when it', 'when his',
        'when her', 'when their', 'when its', 'when it\'s', 'when that', 'when\'s',
    'how is', 'how are', 'how did', 'how\'s',
    'where is', 'where are', 'where did', 'where\'s',
    'how do', 'how does', 'how can', 'how will', 'how did'
];

const allQuestionWords = boolQuestionWords.concat(otherQuestionWords);

const questionWords = {
    bool : boolQuestionWords,
    other : otherQuestionWords,
    all : allQuestionWords
};

const emotions = ['happy', 'sad', 'angry', 'nervous', 'scared', 'excited', 'anxious'];

const waysToFeel = ['rather fine', 'ok', 'great', 'not bad', 'excellent'];

const allFeelings = emotions.concat(waysToFeel);

const likedFoods = ['ice-cream', 'ice cream', 'pie', 'pies', 'apricots', 'apricots', 'fruit', 'fruits',
    'pasta', 'pizza', 'cake', 'bread', 'tofu', 'pasties', 'orange', 'oranges',
    'noodles', 'soup', 'potato', 'potatoes', 'carrot', 'carrots', 'pea', 'peas'
];

const likedOtherThings = [
    'book', 'books', 'coding', 
    'computer', 'computers', 'winter', 'plane', 'planes', 'aircraft', 'aeroplane', 'aeroplanes', 
    'airplane', 'airplanes', 'flight', 'flying', 'plant', 'plants', 'tree', 'trees', 'math', 
    'ostriches', 'pig', 'pigs', 'tennis', 'science', 'lego', 'brain', 'brains', 'smart', 
    'smartness', 'ostrich', 'art', 'wealth', 'money', 'hat', 'award',
    'party', 'prize', 'festival', 'food', 'rockets',  'water', 'premium', 'orange juice',
    'laptop', 'chromebook', 'virtual linux machine', 'clock', 'clocks', 'green', 'blue',
    'flight', 'ravi', 'dominic', 'nguyen'
];

const likedThings = likedOtherThings.concat(likedFoods);

const dislikedThings = [
    'summer', 'meat', 'pork', 'bacon', 'beef', 'mutton', 'cream', 'soccer', 'football', 'dairy', 
    'milk', 'mum', 'stapler', 'bored', 'heat', 'pink', 'purple', 'diesel planes', 'trucks', 'f-104', 
    'f 104', 'starfighter', 'vomit', 'arms', 'legos', 'legoes', 'poo', 'poos', 'poop', 'poops', 'pooping', 
    'punch', 'punches', 'punched', 'punching', 'fart', 'farted', 'farting', 'farter', 'farts',
    'office', 'guitar', 'death', 'socks', 'pigsty', 'publicity', 'apples juice', 'functional programming',
    'traitor'
];

const niceWords = [
    'happy', 'glad', 'nice', 'great', 'good', 'thrilling', 'love', 'awesome', 'cool', 'polite',
    'pleased', 'joy', 'enjoy', 'enjoyed', 'enjoyable', 'joyful', 'cheery', 'fun', 'funny', 'dear', 'awesome',
    'super', 'beautiful', 'pretty', 'tasty', 'yummy', 'lovely', 'positive', 'right', 'correct',
    'perfect', 'shiny', 'new', 'futuristic', 'fantastic', 'strong', 'powerful', 'amazing'
];
const meanWords = [
    'sad', 'angry', 'unhappy', 'bad', 'mediocre', 'silly', 'negative', 'impractical',
    'stupid', 'evil', 'ugly', 'fat', 'smell', 'smelly', 'grumpy', 'stink', 'wrong', 'weak',
    'stinky', 'hate', 'boring', 'mean', 'jump in a lake', 'jump off a cliff', 'weird', 'betray',
    'pathetic', 'terrible', 'horrendous', 'horrible', 'awful', 'apalling', 'fat', 'baka', 'fail',
    'get stuffed', 'kill', 'kills', 'killer', 'killing', 'killers', 'lonely', 'depressed', 'desperate',
    'shut up', 'annoy', 'annoying', 'annoys', 'annoyed',
    'die', 'idiot', 'idiotic', 'rude', 'tired', 'dumb', 'dumber', 'dumbest', 'dumbo', 'yeet', 'yoink', 'yate'
]; // I regret even typing those last three words! It's better than the chatbot liking them though.

// replies
// -------

const confusedStatementReplies = ['Why\'s that?', 'Ok...', 'If you say so', 'I guess', 'that\'s weird',
'I don\'t care', 'tidak kamu', 'bla', 'says you', 'say what?', 'I mean, why not', 'Pardon?'];

const positiveStatementReplies = {
    'user' : ['Great!', 'I\'m glad to hear that', 'Cooooool', 'Nice!', 'Awesome', 'Not bad', 'Sweet!'],
    'otherObj' : ['Great!', 'I\'m glad to hear that', 'Cooooool', 'Nice!', 'Awesome', 'Not bad', 'Sweet!'],
    'self' : ['Why, thanks', 'Thanks']
};

const negativeStatementReplies = {
    'user' : ['I\'m sorry to hear that', 'What a pity', 'Awww man!'],
    'otherObj' : ['\'m sorry to hear that', 'What a pity', 'Awww man!'],
    'self' : ['That\'s not very nice', 'You\'re mean', 'Waaah!', 'Meanie!']
};

const statementReplies = {
    confused : confusedStatementReplies,
    positive : positiveStatementReplies,
    negative : negativeStatementReplies
}

const greetingReplies = ['Hi', 'Good day', 'Hello', 'G\'day', 'And a good morning to you',
    'Good morning', 'Good evening', 'Good night', 'Hey!', 'Hi! How are you?', 'Hello, how are you going?'
];
const farewellReplies = ['See ya', 'See you', 'Bye!', 'Goodbye', 'Bye-bye', 'See you later', 'See ya mate',
    'Farewell, dearest friend', 'Good riddance!', 'Finally, you\'re going'];

const confusedQuestionReplies = ['I don\'t know', 'You\'re asking me?', 'Well, it depends',
    'That\'s a tricky one', 'Why do you ask me?', 'How should I know?', 'Ask yourself why don\'t you'];

const positiveQuestionReplies = ['Yes', 'Of course!', 'What made you doubt it?', 'Definitely'];

const negativeQuestionReplies = ['No', 'NO WAY!', 'Of course not!', 'Nope'];

const insultedReplyStarts = ['How rude!', 'How dare you insult me?']
const insultedReplyEnds = ['I\'m going!', 'Good riddance!']

const insultedReplies = {
    starts : insultedReplyStarts,
    ends : insultedReplyEnds
}


// these are functions so that some can be randomised etc
const selfInquiryReplies = { // don't forget to change setName for the top two or more
    'your name' : () => {return 'Chatbot'},
    'who are you' : () => {return 'Chatbot'},
    'age' : () => {return 'I don\'t have an age (I\'m a computer, idiot)'},
    'old' : () => {return'I don\'t have an age (I\'m a computer, idiot)'},

    'mother' : () => {return 'No idea whatsoever'}, 
    'mum' : () => {return 'No idea whatsoever'}, 
    'mom' : () => {return 'No idea whatsoever'},
    'father' : () => {return 'My dad might be the old python chatbot'},
    'dad' : () => {return 'My dad might be the old python chatbot'},
    'creator' : () => {return 'The great Ravi A. Bonincontro, who must be respected at all times'},
    'creater' : () => {return 'The great Ravi A. Bonincontro, who must be respected at all times'},
    'master' : () => {return 'The same as my creator'},
    'live' : () => {return 'In this computer'},

    'how are you' : () => {return choice(waysToFeel)},
    'are you ok' : () => {return 'Yes'},
    'are you okay' : () => {return 'Yes'},
    'how do you feel' : () => {return choice(emotions)},
    'happy' : () => {return 'Of course!'},
    'sad' : () => {return 'I am never sad'},

    'have for breakfast' : () => {return choice(likedFoods)},
    'have for lunch' : () => {return choice(likedFoods)},
    'have for dinner' : () => {return choice(likedFoods)},

    'eat' : () => {return choice(likedFoods)}
}

function setName(name) {
    selfInquiryReplies['your name'] = () => {return name};
    selfInquiryReplies['who are you'] = () => {return name};
}

const questionReplies = {
    confused : confusedQuestionReplies,
    positive : positiveQuestionReplies,
    negative : negativeQuestionReplies
}

// enums
// -----
const fuzzyAnswers = {
    no : 'no',
    maybe : 'maybe',
    yes : 'yes'
}

const sentenceTypes = {
    statement : 'statement',
    question : 'question',
    greeting : 'greeting'
}

const questionTypes = {
    selfInquiry : 'selfInquiry',
    userInquiry : 'userInquiry',
    boolInquiry : 'boolInquiry',
    noIdeaInquiry : 'noIdeaInquiry',
    otherInquiry : 'otherInquiry'
}

const subjects = {
    user : 'user',
    self : 'self',
    otherObj : 'otherObj'
}

// util functions
// --------------

function randint(min, max) {
    var diff = max - min;
    return Math.floor(Math.random() * diff + min);
}

function choice(list) {
    var idx = randint(0, list.length);
    return list[idx];
}

function countWholeWordOccurencesList(str, substrList) {
    // counts the total of all the substrs in substrList - not just a single substr
    var total = 0;
    for (var i = 0; i < substrList.length; i ++) {
        total += countWholeWordOccurences(str, substrList[i]);
    }
    return total;
}

function countWholeWordOccurences(str, substr) {
    // split the substring into words then remove spaces - pass that off to the more basic function as a phrase
    // (the basic function splits str)

    var substrWords = substr.split(/([_\W])/); // split into words (forgot exactly what this does but it works)
    substrWords = removeAllFromArray(substrWords, ' '); // remove the spaces

    return countMultiWordPhrases(str, substrWords);
}

function countMultiWordPhrases(str, wordList) {
    var words = str.split(/([_\W])/); // split into words (forgot exactly what this does but it works)
    words = removeAllFromArray(words, ' '); // remove the spaces

    if (str == 'good' && wordList.includes('good')) var isdebugging = true;

    var count = 0;
    for (var i = 0; i < words.length; i ++) {
        var nextNWords = words.slice(i, i + wordList.length);
        if (itemsEqual(wordList, nextNWords)) {
            count ++;
        }
    }
    return count;
}

function removeAllFromArray(array, itemToRemove) {
    // uses tight checking
    var newArray = []
    for (var i = 0; i < array.length; i ++) {
        if (array[i] !== itemToRemove) newArray.push(array[i]);
    }
    return newArray;
}

function itemsEqual(arr, arr2) {
    // if the arrays are not the same length, it will return false
    if (arr.length !== arr2.length) return false;

    var equal = true;

    for (var i = 0; i < arr.length; i ++) {
        if (arr[i] != arr2[i]) {
            equal = false;
            break;
        }
    }
    return equal;
}

function defaultQuit(time) {
    setTimeout(() => location = 'about:blank', time);
}

// main class
// ----------

export class Chatbot {
    constructor(name='Chatbot', quitFunc=defaultQuit) {
        this.name = name;
        setName(this.name);

        this.cmdKeyword = 'cmd:';

        this.insultedLevel = 0;
        this.insultedMin = 0;
        this.insultedMax = 5;

        this.quit = quitFunc;

        this.keywords = {
            userRelated : userRelatedKeywords,
            selfRelated : selfRelatedKeywords,
            objectRelated : objectRelatedKeywords,
            likedThings : likedThings,
            dislikedThings : dislikedThings,
            niceWords : niceWords,
            meanWords : meanWords,
            greetings : greetings,
            farewells : farewells,
            questionWords : questionWords
        };

        this.replies = {
            statement : statementReplies,
            question : questionReplies,
            greeting : greetingReplies,
            farewell : farewellReplies,
            insulted : insultedReplies,
            selfInquiry : selfInquiryReplies
        }
    }

    processSentence(userInput) {
        userInput = userInput.toLowerCase(); // make it lowercase right at the start as this program doesn't care about capitals
        var sentenceIsSpecial = this.isSentenceSpecial(userInput);
        
        if (sentenceIsSpecial == 'no') {
            var meaningFlipped = this.doNegativesFlip(userInput); // whether the nots flip the sentence's meaning 
    
            var subject = this.findSubject(userInput);
            var sentencePositive = this.isSentencePositive(userInput); // whether the sentence not including the nots has a positive meaning. a fuzzyAnswer
            var sentenceType = this.findSentenceType(userInput);
        
            var reply = this.makeReply(userInput, meaningFlipped, subject, sentencePositive, sentenceType);
            
            var shouldQuit = this.getInsulted(meaningFlipped, subject, sentencePositive, sentenceType);

            if (shouldQuit) {
                // make an insulted reply then quit
                reply = choice(this.replies.insulted.starts) + ' ' + choice(this.replies.insulted.ends);
                this.quit(3000);
            }

            return reply;
        }
        
        else if (sentenceIsSpecial == 'command') {
            return 'Commands are currently not supported';
        }
        
        else if (sentenceIsSpecial == 'quit') {
            this.quit(500);
        }

        else if (sentenceIsSpecial == 'go away') {
            this.quit(1500);
            return 'Ok, if you wish';
        }
    }

    makeReply(sentence, meaningFlipped, subject, sentencePositive, sentenceType) {
        if (sentenceType == sentenceTypes.statement) {
            return this.replyToStatement(meaningFlipped, subject, sentencePositive);
        }
        else if (sentenceType == sentenceTypes.question) {
            return this.replyToQuestion(sentence, meaningFlipped, subject, sentencePositive);
        }
        else if (sentenceType == sentenceTypes.greeting) {
            return choice(this.replies.greeting);
        }
        else if (sentenceType == sentenceTypes.farewell) {
            return choice(this.replies.farewell);
        }
    }

    replyToStatement(meaningFlipped, subject, sentencePositive) {
        if (sentencePositive == fuzzyAnswers.maybe) {
            return choice(this.replies.statement.confused);
        }
        else {
            sentencePositive = this.flipMeaning(meaningFlipped, sentencePositive);
            if (sentencePositive == fuzzyAnswers.yes) {
                var replyList = this.replies.statement.positive[subject];
            }
            else {
                var replyList = this.replies.statement.negative[subject];
            }
            return choice(replyList);
        }
    }

    replyToQuestion(sentence, meaningFlipped, subject, sentencePositive) {
        if (subject == subjects.user || subject == subjects.otherObj) {
            return choice(this.replies.question.confused);
        }
        else {
            var questionType = this.findQuestionType(sentence, subject);
            if (questionType == questionTypes.selfInquiry) {
                return this.replyToSelfInquiry(sentence, meaningFlipped);
            }
            else if (questionType == questionTypes.boolInquiry) {
                sentencePositive = this.flipMeaning(meaningFlipped, sentencePositive);
                if (sentencePositive == fuzzyAnswers.yes) {
                    return choice(this.replies.question.positive);
                }
                else if (sentencePositive == fuzzyAnswers.maybe) {
                    return choice(this.replies.question.confused);
                }
                else {
                    return choice(this.replies.question.negative)
                }
            }
            else {
                return choice(this.replies.question.confused);
            }
        }
    }

    replyToSelfInquiry(sentence, meaningFlipped) {
        if (meaningFlipped) {
            return choice(this.replies.question.confused);
        }
        else {
            var reply = choice(this.replies.question.confused);
            
            var attrsFound = this.findSelfAttrs(sentence);
            var possibleReplyMaker = this.replies.selfInquiry[attrsFound[0]]
            if (possibleReplyMaker !== undefined) {
                reply = possibleReplyMaker();
            }
            return reply;
        }
    }

    findSubject(sentence) {
        // finds the subject of the sentence - whether it's the user or the chatbox

        var subject = null;
        for (var i = 0; i < this.keywords.userRelated.length; i ++) {
            var occurences = countWholeWordOccurences(sentence, this.keywords.userRelated[i]);
            if (occurences > 0) subject = subjects.user;
        }

        for (var i = 0; i < this.keywords.objectRelated.length; i ++) {
            var occurences = countWholeWordOccurences(sentence, this.keywords.objectRelated[i]);
            if (occurences > 0) subject = subjects.otherObj;
        }

        for (var i = 0; i < this.keywords.selfRelated.length; i ++) {
            var occurences = countWholeWordOccurences(sentence, this.keywords.selfRelated[i]);
            if (occurences > 0) subject = subjects.self;
        }
        
        if (subject === null) subject = subjects.self;
        return subject;
    }

    flipMeaning(meaningFlipped, sentencePositive) {
        if (meaningFlipped) {
            if (sentencePositive == fuzzyAnswers.yes) {
                return fuzzyAnswers.no;
            }
            else {
                return fuzzyAnswers.yes;
            }
        }
        else {
            return sentencePositive;
        }
    }

    findSentenceType(sentence) {
        var sentenceType = sentenceTypes.statement;

        var endsWithPunctuation = !!sentence.match(/[.,!?]$/);
        if (endsWithPunctuation) {
            var lastChar = sentence[sentence.length - 1];
            if (lastChar == '?') {
                sentenceType = sentenceTypes.question;
            }
            else {
                sentenceType = sentenceTypes.statement;
            }
        }
        else {
            var totalQuestionWords = 0;
            for (var i = 0; i < this.keywords.questionWords.all.length; i ++) {
                totalQuestionWords += countWholeWordOccurences(sentence, this.keywords.questionWords.all[i]);
            }
            if (totalQuestionWords > 0) {
                sentenceType = sentenceTypes.question;
            }
            else {
                sentenceType = sentenceTypes.statement;
            }
        }

        if (sentenceType !== sentenceTypes.question) {
            var greetingsTotal = 0;
            this.keywords.greetings.forEach(greet => {
                greetingsTotal += countWholeWordOccurences(sentence, greet);
            });
            
            var minGreetingsNeeded = sentence.length / 20;
            if (greetingsTotal > minGreetingsNeeded && greetingsTotal > 0) {
                sentenceType = sentenceTypes.greeting;
            }

            var farewellsTotal = 0;
            this.keywords.farewells.forEach(farewell => {
                farewellsTotal += countWholeWordOccurences(sentence, farewell);
            });
            
            var minfarewellsNeeded = sentence.length / 20;
            if (farewellsTotal > minfarewellsNeeded) {
                sentenceType = sentenceTypes.farewell;
            }
        }

        return sentenceType;
    }

    findQuestionType(subject) {
        if (subject == subjects.self) {
            return questionTypes.selfInquiry;
        }
        else {
            return questionTypes.otherInquiry;
        }
    }

    isSentencePositive(sentence) {
        // find whether the sentence makes the chatbot happy/whether the chatbox agrees with it
        
        var positiveWords = this.keywords.likedThings.concat(this.keywords.niceWords);
        var negativeWords = this.keywords.dislikedThings.concat(this.keywords.meanWords);

        var positiveWordTotal = 0;
        var negativeWordTotal = 0;

        for (var i = 0; i < positiveWords.length; i ++) {
            var crntPositiveWord = positiveWords[i];
            positiveWordTotal += countWholeWordOccurences(sentence, crntPositiveWord);
        }

        for (var i = 0; i < negativeWords.length; i ++) {
            var crntNegativeWord = negativeWords[i];
            negativeWordTotal += countWholeWordOccurences(sentence, crntNegativeWord);
        }

        if (positiveWordTotal > negativeWordTotal) return fuzzyAnswers.yes;
        else if (positiveWordTotal < negativeWordTotal) return fuzzyAnswers.no;
        else return fuzzyAnswers.maybe;
    }

    findSelfAttrs(sentence) {
        var foundAttributes = [];
        var knownAttributes = Object.keys(this.replies.selfInquiry);
        for (var attr = 0; attr < knownAttributes.length; attr ++) {
            var attrsFound = countWholeWordOccurences(sentence, knownAttributes[attr]);
            if (attrsFound > 0) foundAttributes.push(knownAttributes[attr]);
        }
        return foundAttributes
    }

    findQuestionType(sentence, subject) {
        var questionType = questionTypes.noIdeaInquiry;
        if (subject == subjects.self) {
            var foundAttributes = this.findSelfAttrs(sentence);
            if (foundAttributes.length > 0) {
                questionType = questionTypes.selfInquiry;
            }
            else {
                var foundBoolAsks = countWholeWordOccurencesList(sentence, this.keywords.questionWords.bool);
                var foundOtherAsks = countWholeWordOccurencesList(sentence, this.keywords.questionWords.other);
                if (foundBoolAsks > foundOtherAsks) questionType = questionTypes.boolInquiry;
                else questionType = questionTypes.noIdeaInquiry;
            }
        }
        return questionType;
    }

    doNegativesFlip(sentence) {
        // checks whether the overall meaning of the sentence is what is says or is flipped (based on how many nots)
        var nots = countWholeWordOccurences(sentence, 'not');
        var donts = countWholeWordOccurences(sentence, 'don\'t');
        var nevers = countWholeWordOccurences(sentence, 'never');
        var nos = countWholeWordOccurences(sentence, 'no');

        var total = nots + donts + nevers + nos;
        if (total % 2 == 0) { // if there are an even amount of negatives
            return false;
        }
        else {
            return true;
        }
    }

    isSentenceSpecial(sentence) {
        if (sentence.substring(0, this.cmdKeyword.length) == this.cmdKeyword) {
            return 'command';
        }
        else if (sentence == 'quit') {
            return 'quit';
        }
        else if (sentence.includes('go away')) {
            return 'go away';
        }
        else {
            return 'no';
        }
    }

    getInsulted(meaningFlipped, subject, sentencePositive, sentenceType) {
        var shouldQuit = false;
        if (sentencePositive != fuzzyAnswers.maybe && sentenceType == sentenceTypes.statement) {
            sentencePositive = this.flipMeaning(meaningFlipped, sentencePositive);

            // if it's not a nice sentence and it's referring to self, BE INSULTED!
            if (sentencePositive == fuzzyAnswers.no && subject == subjects.self) {
                this.insultedLevel += 1;
                if (this.insultedLevel >= this.insultedMax) {
                    shouldQuit = true;
                }
            }
            else {
                this.insultedLevel -= 0.5;
                if (this.insultedLevel < this.insultedMin) this.insultedLevel = this.insultedMin;
            }
        }
        return shouldQuit;
    }
}