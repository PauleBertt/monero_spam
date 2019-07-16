#!/usr/bin/env bash#!/usr/bin/env bash
./monero_files/monero-wallet-rpc --daemon-address 127.0.0.1:48081 --max-concurrency 8 --log-file stage_log.log --password-file monero_files/wallet_password.txt --rpc-bind-ip 127.0.0.1 --rpc-bind-port 18083 --rpc-login test:123456 --stagenet --wallet-file monero_files/stage_wallet
