{ pkgs ? import <nixpkgs> { } }:

with pkgs;
let
  customPython = pkgs.python39.buildEnv.override {
    extraLibs = with pkgs.python39Packages; [ pillow ];
  };
in

pkgs.mkShell {
  buildInputs = (import ./build-inputs.nix) { inherit pkgs; };
}
