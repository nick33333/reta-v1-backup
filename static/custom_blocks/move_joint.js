Blockly.Blocks['move_to'] = {
    init: function() {
      this.appendValueInput("j1")
          .setCheck("Number")
          .appendField("Move To:  ")
          .appendField("j1");
      this.appendValueInput("j2")
          .setCheck("Number")
          .appendField("j2");
      this.appendValueInput("j3")
          .setCheck("Number")
          .appendField("j3");
      this.setInputsInline(true);
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(230);
   this.setTooltip("");
   this.setHelpUrl("");
    }
  };