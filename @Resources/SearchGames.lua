-- Define global tables to store game information
local gamesInfo = {}
local gameIDs = {}
local nonSteamGames = {}

function Update()
    -- Set Variables
    searchInput = SKIN:GetVariable("SearchInput")
    scriptPath = SKIN:GetVariable("@")
    gamesInfoPath = scriptPath .. "GamesInfo.inc"
    nonSteamGamesPath = scriptPath .. "NonSteamGames.inc"

    -- Populate Tables
    if not next(gameIDs) then
        gameIDs, _, _ = ReadGameInfo(gamesInfoPath)
    end
    if not next(gamesInfo) then
        _, gamesInfo, _ = ReadGameInfo(gamesInfoPath)
    end
    if not next(nonSteamGames) then
        _, _, nonSteamGames = ReadGameInfo(nonSteamGamesPath)
    end
    
    -- Match based on ID or Name
    local result = nil
    if tonumber(searchInput) then
        result = GetGameInfoByID(searchInput)
    else
        result = GetGameInfoByName(searchInput)
    end
    
    -- Update Rainmeter skin based on the result
    if result then
        SKIN:Bang('!SetVariable', 'SearchResults', result)
        SKIN:Bang('!UpdateMeter', 'BG')
        SKIN:Bang('!UpdateMeasure', 'Lenght')
        SKIN:Bang('!ReDraw')
    else
        SKIN:Bang('!ShowMeter', 'MatchText')
        SKIN:Bang('!ReDraw')
    end
end

-- Function to read game information from a file into tables
function ReadGameInfo(filePath)
    local gamesInfoTable = {}
    local gameIDsTable = {}
    local nonSteamGamesTable = {}

    local file, err = io.open(filePath, "r")
    if not file then
        print("Error opening file:", err)
        return gamesInfoTable, nonSteamGamesTable
    end

    for line in file:lines() do
        local i, ID = line:match('ID(%d+)=([^"]+)')
        local id, name = line:match('ID(%d+)name="([^"]+)"')
        local egame, gameValue = line:match('Egame(%d+)="([^"]+)"')

        if i and ID then
            gameIDsTable[i] = ID
        elseif id and name then
            gamesInfoTable[id] = name
        elseif egame and gameValue then
            nonSteamGamesTable[egame] = gameValue
        end
    end
    file:close()
    return gameIDsTable, gamesInfoTable, nonSteamGamesTable
end

-- Function to get game information by ID
function GetGameInfoByID(gameID)
    for i, ID in pairs(gameIDs) do
        if ID == gameID then
            SKIN:Bang('!ShowMeterGroup', 'G' .. i)
            gameCount = gameCount + 1
            result = gameCount
            return result
        end
    end
end

function GetGameInfoByName(gameName)
    local gameCount = 0
    local result = nil

    for id, name in pairs(gamesInfo) do
        local normalizedSkinName = NormalizeString(gameName)
        local normalizedFileName = NormalizeString(name)
        if StringContains(normalizedFileName, normalizedSkinName) then
            SKIN:Bang('!ShowMeterGroup', 'G' .. id)
            gameCount = gameCount + 1
        end
    end
    for egame, gameValue in pairs(nonSteamGames) do
        local normalizedSkinName = NormalizeString(gameName)
        local normalizedFileName = NormalizeString(gameValue)
        if StringContains(normalizedFileName, normalizedSkinName) then
            SKIN:Bang('!ShowMeterGroup', 'EG' .. egame)
            gameCount = gameCount + 1
        end
    end
    if gameCount > 0 then
        result = gameCount
        return result
    end
end

-- Function to find Str in Str
function StringContains(str, substr)
    return string.find(str, substr, 1, true) ~= nil
end

-- Helper function to normalize a string (remove spaces and special characters)
function NormalizeString(inputString)
    if type(inputString) == "number" then
        inputString = tostring(inputString)
    end
    return inputString:gsub("[%s%p]", ""):lower()
end

-- Function to read file
function ReadFileContent(filePath)
    local file, err = io.open(filePath, "r")
    if not file then
        print("Error opening file:", err)
        return nil
    end
    local content = file:read("*all")
    file:close()
    return content
end