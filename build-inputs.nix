{ pkgs ? import <nixpkgs> { } }:

with pkgs;
let
  customPython = pkgs.python39.buildEnv.override {
    extraLibs = with pkgs.python39Packages; [ blessed selenium livereload];
  };
in
[ clang cmake customPython geckodriver firefox chromedriver google-chrome chromium ]
