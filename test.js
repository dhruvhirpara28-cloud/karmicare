function testParsing() {
    var text = "+20% Return on Care";
    var match = text.match(/(\d+)%/);
    return match ? match[1] : null;
}
testParsing();
