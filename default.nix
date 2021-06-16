{ pkgs, nixpkgs }:
let
  lib           = nixpkgs.lib;
in
pkgs.pkgs.stdenv.mkDerivation rec {
  pname       = "auto-bg";
  version     = "0.0.1";
# dontUnpack  = true;
  unpackPhase = "true";
  buildInputs = (import ./build-inputs.nix) { inherit pkgs; };

  buildPhase  = ''
  '';
  installPhase = ''
    mkdir -p $out/bin
    cp ${./gen_wall.py} $out/bin/gen_wall
    chmod +x $out/bin/gen_wall
  '';
    #mv ./gen_wall.py "$out/bin/gen_wall.py"
}
