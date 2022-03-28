Blockly.Blocks['power_down'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Shut Down Robot");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(345);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };