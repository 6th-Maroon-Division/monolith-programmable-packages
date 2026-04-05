local bios = {}

function bios.version()
  return "1.0.0"
end

function bios.boot()
  return true, "bios-core booted"
end

return bios
