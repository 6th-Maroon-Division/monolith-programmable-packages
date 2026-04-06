term.writeLine('=== Pump Comprehensive Test ===')
term.writeLine('')

local devices = atmos.list()
if devices == nil or #devices == 0 then
    term.writeLine('No linked atmos devices found.')
    term.writeLine('Use the linker tool and then open the computer device manager.')
    return
end

local pumps = {}

term.writeLine('Linked devices:')
for i = 1, #devices do
    local device = devices[i]
    local label = tostring(device.label or '?')
    local kind = tostring(device.type or 'unknown')
    local address = tostring(device.address or '?')

    term.writeLine('  [' .. kind .. '] ' .. label .. ' @ ' .. address)

    if kind == 'pressure_pump' or kind == 'volume_pump' then
        pumps[#pumps + 1] = label
    end
end

if #pumps == 0 then
    term.writeLine('')
    term.writeLine('No linked pumps found.')
    return
end

term.writeLine('')
term.writeLine('=== Testing ' .. tostring(#pumps) .. ' pump(s) ===')

local warnedNoSleep = false

local function waitSeconds(seconds)
    if type(os) == 'table' and type(os.sleep) == 'function' then
        os.sleep(seconds)
        return
    end

    if not warnedNoSleep then
        term.writeLine('  Note: timed sleep API is unavailable; continuing without delay.')
        warnedNoSleep = true
    end
end

local function printPumpState(label)
    local ok, state = pcall(function()
        return atmos.pump_read(label)
    end)
    
    if ok and state then
        local enabled = state.enabled and 'ON' or 'OFF'
        local info = '  State: ' .. enabled .. ' | Type: ' .. state.type
        
        if state.type == 'volume_pump' then
            info = info .. ' | Rate: ' .. string.format('%.2f', state.transfer_rate) 
                        .. '/' .. string.format('%.2f', state.max_transfer_rate) .. ' L/s'
            if state.overclocked then
                info = info .. ' [OVERCLOCKED]'
            end
        elseif state.type == 'pressure_pump' then
            info = info .. ' | Pressure: ' .. string.format('%.0f', state.target_pressure)
                        .. '/' .. string.format('%.0f', state.max_target_pressure) .. ' kPa'
        end
        
        term.writeLine(info)
    else
        term.writeLine('  Error reading state: ' .. tostring(state))
    end
end

for pumpIdx = 1, #pumps do
    local label = pumps[pumpIdx]
    term.writeLine('')
    term.writeLine('Testing pump: ' .. label)
    term.writeLine('---')
    
    -- Step 1: Turn pump ON
    term.writeLine('[1] Turning pump ON...')
    local ok, err = pcall(function()
        atmos.pump_enabled(label, true)
    end)
    local continuePump = true
    if not ok then
        term.writeLine('ERROR enabling pump: ' .. tostring(err))
        continuePump = false
    end
    if continuePump then
        printPumpState(label)
        
        -- Wait 1 second
        term.writeLine('[2] Waiting 1 second...')
        waitSeconds(1.0)
        
        -- Step 2: Set pump to max
        term.writeLine('[3] Setting to MAX output...')
        local stateOk, state = pcall(function()
            return atmos.pump_read(label)
        end)
        
        if stateOk and state then
            if state.type == 'volume_pump' then
                ok, err = pcall(function()
                    atmos.pump_rate(label, state.max_transfer_rate)
                end)
            elseif state.type == 'pressure_pump' then
                ok, err = pcall(function()
                    atmos.pump_pressure(label, state.max_target_pressure)
                end)
            end
            
            if not ok then
                term.writeLine('ERROR setting max: ' .. tostring(err))
            else
                printPumpState(label)
            end
        end
        
        -- Wait 1 second
        term.writeLine('[4] Waiting 1 second...')
        waitSeconds(1.0)
        
        -- Step 3: Set pump to half max
        term.writeLine('[5] Setting to HALF MAX output...')
        stateOk, state = pcall(function()
            return atmos.pump_read(label)
        end)
        
        if stateOk and state then
            if state.type == 'volume_pump' then
                ok, err = pcall(function()
                    atmos.pump_rate(label, state.max_transfer_rate * 0.5)
                end)
            elseif state.type == 'pressure_pump' then
                ok, err = pcall(function()
                    atmos.pump_pressure(label, state.max_target_pressure * 0.5)
                end)
            end
            
            if not ok then
                term.writeLine('ERROR setting half max: ' .. tostring(err))
            else
                printPumpState(label)
            end
        end
        
        -- Wait 1 second
        term.writeLine('[6] Waiting 1 second...')
        waitSeconds(1.0)
        
        -- Step 4: Turn pump OFF
        term.writeLine('[7] Turning pump OFF...')
        ok, err = pcall(function()
            atmos.pump_enabled(label, false)
        end)
        if not ok then
            term.writeLine('ERROR disabling pump: ' .. tostring(err))
        else
            printPumpState(label)
        end
        
        term.writeLine('[8] Complete!')
    end
end

term.writeLine('')
term.writeLine('=== Test completed ===')
