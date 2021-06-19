{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs;
    flake-utils.url = github:numtide/flake-utils;
  };

  outputs = { nixpkgs, self, flake-utils, ... }@inputs:
    flake-utils.lib.eachDefaultSystem
      (system:
      let 
        #pkgs = nixpkgs.legacyPackages.${system}; 
        pkgs = import nixpkgs {
          config = { allowUnfree = true; };
          inherit system;
        };
      in {
          devShell = import ./shell.nix { inherit pkgs; };
          defaultPackage = pkgs.mkl;
        }
      );
}
