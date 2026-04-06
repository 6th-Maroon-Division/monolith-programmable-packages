term.clear()
term.resetColors()
term.setCursorPos(1, 1)

local function p2(n)
    if n < 10 then
        return '0' .. tostring(n)
    end

    return tostring(n)
end

local function contrast(bg)
    if bg == colors.black or bg == colors.maroon or bg == colors.green or bg == colors.navy or bg == colors.purple or bg == colors.teal or bg == colors.gray then
        return colors.white
    end

    return colors.black
end

local function write_fg_sample(index)
    term.setBackgroundColor(index == colors.black and colors.silver or colors.black)
    term.setTextColor(index)
    term.write(' ' .. p2(index) .. ' ')
    term.resetColors()
end

local function write_bg_sample(index)
    term.setBackgroundColor(index)
    term.setTextColor(contrast(index))
    term.write(' ' .. p2(index) .. ' ')
    term.resetColors()
end

local function write_mix_sample(fg, bg, label)
    term.setBackgroundColor(bg)
    term.setTextColor(fg)
    term.write(' ' .. label .. ' ')
    term.resetColors()
end

term.writeLine('TERM DEBUG: glyphs, fg, bg, mixed')
term.writeLine('lower: abcdefghijklmnopqrstuvwxyz')
term.writeLine('upper: ABCDEFGHIJKLMNOPQRSTUVWXYZ')
term.writeLine('digit: 0123456789')
term.writeLine('sym1 : ' .. [[.,:;!?-_=+/]])
term.writeLine('sym2 : ' .. [[[]{}()<>@#$%^&*|]])
term.writeLine('sym3 : ' .. [[~`]])
term.writeLine('FG palette:')

for i = 0, 7 do
    write_fg_sample(i)
end
term.newLine()
for i = 8, 15 do
    write_fg_sample(i)
end
term.newLine()

term.writeLine('BG palette:')
for i = 0, 7 do
    write_bg_sample(i)
end
term.newLine()
for i = 8, 15 do
    write_bg_sample(i)
end
term.newLine()

term.writeLine('Mixed:')
write_mix_sample(colors.lime, colors.black, 'OK')
write_mix_sample(colors.black, colors.yellow, 'BK')
write_mix_sample(colors.cyan, colors.maroon, 'CY')
write_mix_sample(colors.white, colors.blue, 'WB')
term.newLine()
write_mix_sample(colors.yellow, colors.red, 'YR')
write_mix_sample(colors.magenta, colors.green, 'MG')
write_mix_sample(colors.black, colors.silver, 'BS')
write_mix_sample(colors.red, colors.white, 'RW')
term.newLine()
term.writeLine('Run: termdebug or run /bin/termdebug.lua')
term.resetColors()