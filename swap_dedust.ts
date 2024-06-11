import { Asset, PoolType, ReadinessStatus, VaultJetton, Factory, MAINNET_FACTORY_ADDR } from '@dedust/sdk';
import { Address, toNano } from '@ton/core';
import { TonClient4 } from "@ton/ton";

// Define addresses for HYDRO and USDT
const HYDRO_ADDRESS = Address.parse('EQCbR_BjpDJpolaYfBqkVZQcQWajmCtpKlBbOkSWIuQ3DVtg');
const USDT_ADDRESS = Address.parse('EQDHZDgZjMT8gJazbGj_mzSZDv4QcngZAx57Zx6M1HWJPk5I');

// Create asset instances for HYDRO, TON, and USDT
const HYDRO = Asset.jetton(HYDRO_ADDRESS);
const TON = Asset.native();
const USDT = Asset.jetton(USDT_ADDRESS);

// Open the required pools
const tonClient = new TonClient4({ endpoint: "https://mainnet-v4.tonhubapi.com" });
const factory = tonClient.open(Factory.createFromAddress(MAINNET_FACTORY_ADDR));

const tonHydroPool = tonClient.open(await factory.getPool(PoolType.VOLATILE, [TON, HYDRO]));
const tonUsdtPool = tonClient.open(await factory.getPool(PoolType.VOLATILE, [TON, USDT]));

// Ensure the pools are deployed
if ((await tonHydroPool.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error('Pool (TON, HYDRO) does not exist.');
}

if ((await tonUsdtPool.getReadinessStatus()) !== ReadinessStatus.READY) {
  throw new Error('Pool (TON, USDT) does not exist.');
}

// Find the HYDRO vault
const hydroVault = tonClient.open(await factory.getJettonVault(HYDRO_ADDRESS));

// Find the user's jetton wallet for HYDRO
import { JettonRoot, JettonWallet } from '@dedust/sdk';
const sender = /* Define the sender's address */;
const hydroRoot = tonClient.open(JettonRoot.createFromAddress(HYDRO_ADDRESS));
const hydroWallet = tonClient.open(await hydroRoot.getWallet(sender.address));

// Define the amount to swap
const amountIn = toNano('50'); // 50 HYDRO
const minimalAmountOut = toNano('45'); // Example minimal output for USDT

// Perform the multi-hop swap from HYDRO to USDT via TON
await hydroWallet.sendTransfer(
  sender,
  toNano("0.3"), // 0.3 TON for gas
  {
    amount: amountIn,
    destination: hydroVault.address,
    responseAddress: sender.address, // Return gas to user
    forwardAmount: toNano("0.25"),
    forwardPayload: VaultJetton.createSwapPayload({
      poolAddress: tonHydroPool.address, // First step: HYDRO -> TON
      limit: minimalAmountOut,
      next: {
        poolAddress: tonUsdtPool.address, // Next step: TON -> USDT
      },
    }),
  },
);

console.log('Swap from HYDRO to USDT initiated successfully.');
