let
  pkgs = import <nixpkgs> {};
  etest = import ./default.nix;
in
  pkgs.mkShell {
    inputsFrom = [etest];
    buildInputs = [
      etest
      pkgs.poetry
      pkgs.pre-commit
      pkgs.python38Packages.virtualenv
    ];
    shellHook = ''
      unset SOURCE_DATE_EPOCH
    '';
  }
