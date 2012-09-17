var DCTParser = Editor.Parser = (function() {
    function wordRegexp(words) {
        return new RegExp("^(?:" + words.join("|") + ")$");
    }
    var DELIMITERCLASS = 'dct-delimiter';
    var LITERALCLASS = 'dct-literal';
    var ERRORCLASS = 'dct-error';
    var OPERATORCLASS = 'dct-operator';
    var IDENTIFIERCLASS = 'dct-identifier';
    var STRINGCLASS = 'dct-string';
    var BYTESCLASS = 'dct-bytes';
    var UNICODECLASS = 'dct-unicode';
    var RAWCLASS = 'dct-raw';
    var NORMALCONTEXT = 'normal';
    var STRINGCONTEXT = 'string';
    var singleOperators = '+*/%&|^~<>=';
    var doubleOperators = wordRegexp(['=', '<', '>', 'TIMES',
                                      'BIT', 'PLUS']); 
    var singleDelimiters = '()[]{}@,:`=;';
    var doubleDelimiters = [];
    var tripleDelimiters = wordRegexp([]);
    var singleStarters = singleOperators + singleDelimiters + '=!';
    var doubleStarters = '=<>*/';

    var identifierStarters = /[_A-Za-z?]/;

    var wordOperators = wordRegexp(['and', 'or', 'not', 'implies', 'Inj', 'Func', 'PInj', 'PFun']);
//    var wordOperators = wordRegexp([]);

    var commonkeywords = ['so-exists', 'so-forall', 'forall', 'exists'];
    var variables = /^\?[a-z].*$/;
    var relations = /^\?[A-Z].*$/;

//   var commontypes = ['bool', 'classmethod', 'complex', 'dict', 'enumerate',
//                       'float', 'frozenset', 'int', 'list', 'object',
//                       'property', 'reversed', 'set', 'slice', 'staticmethod',
//                       'str', 'super', 'tuple', 'type'];
    var commontypes = [];

//    var py2 = {'types': ['basestring', 'buffer', 'file', 'long', 'unicode',
//                         'xrange'],
//               'keywords': ['exec', 'print'],
//               'version': 2 };
//    var py3 = {'types': ['bytearray', 'bytes', 'filter', 'map', 'memoryview',
//                         'open', 'range', 'zip'],
//               'keywords': ['nonlocal'],
//               'version': 3};
    var py2 = {'types': [], 'keywords': [], 'version': 2};
    var py3 = {'types': [], 'keywords': [], 'version': 3};

    var py, keywords, types, stringStarters, stringTypes, config;

    function configure(conf) {
        if (!conf.hasOwnProperty('DCTVersion')) {
            conf.DCTVersion = 2;
        }
        if (!conf.hasOwnProperty('strictErrors')) {
            conf.strictErrors = true;
        }
        if (conf.DCTVersion != 2 && conf.DCTVersion != 3) {
            alert('CodeMirror: Unknown DCT Version "' +
                  conf.DCTVersion +
                  '", defaulting to DCT 2.x.');
            conf.DCTVersion = 2;
        }
        if (conf.DCTVersion == 3) {
            py = py3;
            stringStarters = /[\'\"rbRB]/;
            stringTypes = /[rb]/;
        } else {
            py = py2;
            stringStarters = /[\'\"RUru]/;
            stringTypes = /[ru]/;
        }
        config = conf;
        keywords = wordRegexp(commonkeywords.concat(py.keywords));
        types = wordRegexp(commontypes.concat(py.types));
        doubleDelimiters = wordRegexp(doubleDelimiters);
    }

    // Mirar aqui el codigo mas de cerca si queremos deteccion sintactica
    // de errores
    var tokenizeDCT = (function() {
        function normal(source, setState) {
            var stringDelim, threeStr, temp, type, word, possible = {};
            var ch = source.next();
            
            function filterPossible(token, styleIfPossible) {
                if (!possible.style && !possible.content) {
                    return token;
                } else if (typeof(token) == STRINGCONTEXT) {
                    token = {content: source.get(), style: token};
                }
                if (possible.style || styleIfPossible) {
                    token.style = styleIfPossible ? styleIfPossible : possible.style;
                }
                if (possible.content) {
                    token.content = possible.content + token.content;
                }
                possible = {};
                return token;
            }

            // Handle comments
            if (ch == ';') {
                while (!source.endOfLine()) {
                    source.next();
                }
                return 'dct-comment';
            }
            // Handle special chars
            if (ch == '\\') {
                if (!source.endOfLine()) {
                    var whitespace = true;
                    while (!source.endOfLine()) {
                        if(!(/[\s\u00a0]/.test(source.next()))) {
                            whitespace = false;
                        }
                    }
                    if (!whitespace) {
                        return ERRORCLASS;
                    }
                }
                return 'dct-special';
            }
            // Handle operators and delimiters
            if (singleStarters.indexOf(ch) != -1 || (ch == "." && !source.matches(/\d/))) {
                if (doubleStarters.indexOf(source.peek()) != -1) {
                    temp = ch + source.peek();
                    // It must be a double delimiter or operator or triple delimiter
                    if (doubleOperators.test(temp)) {
                        source.next();
                        var nextChar = source.peek();
                        if (nextChar && tripleDelimiters.test(temp + nextChar)) {
                            source.next();
                            return DELIMITERCLASS;
                        } else {
                            return OPERATORCLASS;
                        }
                    } else if (doubleDelimiters.test(temp)) {
                        source.next();
                        return DELIMITERCLASS;
                    }
                }
                // It must be a single delimiter or operator
                if (singleOperators.indexOf(ch) != -1 || ch == ".") {
                    return OPERATORCLASS;
                } else if (singleDelimiters.indexOf(ch) != -1) {
                    if (ch == '@' && source.matches(/\w/)) {
                        source.nextWhileMatches(/[\w\d_]/);
                        return {style:'dct-decorator',
                                content: source.get()};
                    } else {
                        return DELIMITERCLASS;
                    }
                } else {
                    return ERRORCLASS;
                }
            }
            // Handle number literals
            if (/\d/.test(ch) || (ch == "." && source.matches(/\d/))) {
                if (ch === '0' && !source.endOfLine()) {
                    switch (source.peek()) {
                        case 'o':
                        case 'O':
                            source.next();
                            source.nextWhileMatches(/[0-7]/);
                            return filterPossible(LITERALCLASS, ERRORCLASS);
                        case 'x':
                        case 'X':
                            source.next();
                            source.nextWhileMatches(/[0-9A-Fa-f]/);
                            return filterPossible(LITERALCLASS, ERRORCLASS);
                        case 'b':
                        case 'B':
                            source.next();
                            source.nextWhileMatches(/[01]/);
                            return filterPossible(LITERALCLASS, ERRORCLASS);
                    }
                }
                source.nextWhileMatches(/\d/);
                if (ch != '.' && source.peek() == '.') {
                    source.next();
                    source.nextWhileMatches(/\d/);
                }
                // Grab an exponent
                if (source.matches(/e/i)) {
                    source.next();
                    if (source.peek() == '+') {
                        source.next();
                    }
                    if (source.matches(/\d/)) {
                        source.nextWhileMatches(/\d/);
                    } else {
                        return filterPossible(ERRORCLASS);
                    }
                }
                // Grab a complex number
                if (source.matches(/j/i)) {
                    source.next();
                }

                return filterPossible(LITERALCLASS);
            }
            // Handle strings
            if (stringStarters.test(ch)) {
                var peek = source.peek();
                var stringType = STRINGCLASS;
                if ((stringTypes.test(ch)) && (peek == '"' || peek == "'")) {
                    switch (ch.toLowerCase()) {
                        case 'b':
                            stringType = BYTESCLASS;
                            break;
                        case 'r':
                            stringType = RAWCLASS;
                            break;
                        case 'u':
                            stringType = UNICODECLASS;
                            break;
                    }
                    ch = source.next();
                    stringDelim = ch;
                    if (source.peek() != stringDelim) {
                        setState(inString(stringType, stringDelim));
                        return null;
                    } else {
                        source.next();
                        if (source.peek() == stringDelim) {
                            source.next();
                            threeStr = stringDelim + stringDelim + stringDelim;
                            setState(inString(stringType, threeStr));
                            return null;
                        } else {
                            return stringType;
                        }
                    }
                } else if (ch == "'" || ch == '"') {
                    stringDelim = ch;
                    if (source.peek() != stringDelim) {
                        setState(inString(stringType, stringDelim));
                        return null;
                    } else {
                        source.next();
                        if (source.peek() == stringDelim) {
                            source.next();
                            threeStr = stringDelim + stringDelim + stringDelim;
                            setState(inString(stringType, threeStr));
                            return null;
                        } else {
                            return stringType;
                        }
                    }
                }
            }
            // Handle Identifier
            if (identifierStarters.test(ch)) {
                source.nextWhileMatches(/[-\w\d_]/);
                word = source.get();
                if (wordOperators.test(word)) {
                    type = OPERATORCLASS;
                } else if (keywords.test(word)) {
                    type = 'dct-keyword';
                } else if (types.test(word)) {
                    type = 'dct-type';
                } else if (relations.test(word)) {
                    type = 'dct-type';
                } else if (variables.test(word)) {
                    type = IDENTIFIERCLASS;
                }
//                    while (source.peek() == '.') {
//                        source.next();
//                        if (source.matches(identifierStarters)) {
//                            source.nextWhileMatches(/[\w\d]/);
//                        } else {
//                            type = ERRORCLASS;
//                            break;
//                        }
//                    }
//                    word = word + source.get();
                return filterPossible({style: type, content: word});
            }

            // Register Dollar sign and Question mark as errors. Always!
            if (/(\$|papa)/.test(ch)) {
                return filterPossible(ERRORCLASS);
            }

            return filterPossible(ERRORCLASS);
        }

        function inString(style, terminator) {
            return function(source, setState) {
                var matches = [];
                var found = false;
                while (!found && !source.endOfLine()) {
                    var ch = source.next(), newMatches = [];
                    // Skip escaped characters
                    if (ch == '\\') {
                        if (source.peek() == '\n') {
                            break;
                        }
                        ch = source.next();
                    }
                    if (ch == terminator.charAt(0)) {
                        matches.push(terminator);
                    }
                    for (var i = 0; i < matches.length; i++) {
                        var match = matches[i];
                        if (match.charAt(0) == ch) {
                            if (match.length == 1) {
                                setState(normal);
                                found = true;
                                break;
                            } else {
                                newMatches.push(match.slice(1));
                            }
                        }
                    }
                    matches = newMatches;
                }
                return style;
            };
        }

        return function(source, startState) {
            return tokenizer(source, startState || normal);
        };
    })();

    function parseDCT(source, basecolumn) {
        if (!keywords) {
            configure({});
        }
        basecolumn = basecolumn || 0;

        var tokens = tokenizeDCT(source);
        var lastToken = null;
        var column = basecolumn;
        var context = {prev: null,
                       endOfScope: false,
                       startNewScope: false,
                       level: basecolumn,
                       next: null,
                       type: NORMALCONTEXT
                       };

        function pushContext(level, type) {
            type = type ? type : NORMALCONTEXT;
            context = {prev: context,
                       endOfScope: false,
                       startNewScope: false,
                       level: level,
                       next: null,
                       type: type
                       };
        }

        function popContext(remove) {
            remove = remove ? remove : false;
            if (context.prev) {
                if (remove) {
                    context = context.prev;
                    context.next = null;
                } else {
                    context.prev.next = context;
                    context = context.prev;
                }
            }
        }

        function indentDCT(context) {
            var temp;
            return function(nextChars, currentLevel, direction) {
                if (direction === null || direction === undefined) {
                    if (nextChars) {
                        while (context.next) {
                            context = context.next;
                        }
                    }
                    return context.level;
                }
                else if (direction === true) {
                    if (currentLevel == context.level) {
                        if (context.next) {
                            return context.next.level;
                        } else {
                            return context.level;
                        }
                    } else {
                        temp = context;
                        while (temp.prev && temp.prev.level > currentLevel) {
                            temp = temp.prev;
                        }
                        return temp.level;
                    }
                } else if (direction === false) {
                    if (currentLevel > context.level) {
                        return context.level;
                    } else if (context.prev) {
                        temp = context;
                        while (temp.prev && temp.prev.level >= currentLevel) {
                            temp = temp.prev;
                        }
                        if (temp.prev) {
                            return temp.prev.level;
                        } else {
                            return temp.level;
                        }
                    }
                }
                return context.level;
            };
        }

        var iter = {
            next: function() {
                var token = tokens.next();
                var type = token.style;
                var content = token.content;

                if (lastToken) {
                    if (lastToken.content == 'def' && type == IDENTIFIERCLASS) {
                        token.style = 'dct-func';
                    }
                    if (lastToken.content == '\n') {
                        var tempCtx = context;
                        // Check for a different scope
                        if (type == 'whitespace' && context.type == NORMALCONTEXT) {
                            if (token.value.length < context.level) {
                                while (token.value.length < context.level) {
                                    popContext();
                                }

                                if (token.value.length != context.level) {
                                    context = tempCtx;
                                    if (config.strictErrors) {
                                        token.style = ERRORCLASS;
                                    }
                                } else {
                                    context.next = null;
                                }
                            }
                        } else if (context.level !== basecolumn &&
                                   context.type == NORMALCONTEXT) {
                            while (basecolumn !== context.level) {
                                popContext();
                            }

                            if (context.level !== basecolumn) {
                                context = tempCtx;
                                if (config.strictErrors) {
                                    token.style = ERRORCLASS;
                                }
                            }
                        }
                    }
                }

                // Handle Scope Changes
                switch(type) {
                    case STRINGCLASS:
                    case BYTESCLASS:
                    case RAWCLASS:
                    case UNICODECLASS:
                        if (context.type !== STRINGCONTEXT) {
                            pushContext(context.level + 1, STRINGCONTEXT);
                        }
                        break;
                    default:
                        if (context.type === STRINGCONTEXT) {
                            popContext(true);
                        }
                        break;
                }
                switch(content) {
                    case '.':
                    case '@':
                        // These delimiters don't appear by themselves
                        if (content !== token.value) {
                            token.style = ERRORCLASS;
                        }
                        break;
                    case ':':
                        // Colons only delimit scope inside a normal scope
                        if (context.type === NORMALCONTEXT) {
                            context.startNewScope = context.level+indentUnit;
                        }
                        break;
                    case '(':
                    case '[':
                    case '{':
                        // These start a sequence scope
                        pushContext(column + content.length, 'sequence');
                        break;
                    case ')':
                    case ']':
                    case '}':
                        // These end a sequence scope
                        popContext(true);
                        break;
                    case 'pass':
                    case 'return':
                        // These end a normal scope
                        if (context.type === NORMALCONTEXT) {
                            context.endOfScope = true;
                        }
                        break;
                    case '\n':
                        // Reset our column
                        column = basecolumn;
                        // Make any scope changes
                        if (context.endOfScope) {
                            context.endOfScope = false;
                            popContext();
                        } else if (context.startNewScope !== false) {
                            var temp = context.startNewScope;
                            context.startNewScope = false;
                            pushContext(temp, NORMALCONTEXT);
                        }
                        // Newlines require an indentation function wrapped in a closure for proper context.
                        token.indentation = indentDCT(context);
                        break;
                }

                // Keep track of current column for certain scopes.
                if (content != '\n') {
                    column += token.value.length;
                }

                lastToken = token;
                return token;
            },

            copy: function() {
                var _context = context, _tokenState = tokens.state;
                return function(source) {
                    tokens = tokenizeDCT(source, _tokenState);
                    context = _context;
                    return iter;
                };
            }
        };
        return iter;
    }

    return {make: parseDCT,
            electricChars: "",
            configure: configure};
})();
