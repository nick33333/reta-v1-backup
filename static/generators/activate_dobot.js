Blockly.Python['activate_robot'] = function(block) {
    // TODO: Assemble Python into code variable.
    var code = 'from serial.tools import list_ports \nfrom pydobot import Dobot \nport = list_ports.comports()[0].device\ndevice = Dobot(port=port, verbose=False)\n\n';
    return code;
  };