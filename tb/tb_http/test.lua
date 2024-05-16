wrk.method = "POST"

local width = "width=" .. string.rep("2", 2048)  -- 2047 bytes for width value
local height = "height=" .. string.rep("2", 2048)  -- 2047 bytes for height value

wrk.body = width .. "&" .. height

wrk.headers['Content-Type'] = "application/x-www-form-urlencoded"
