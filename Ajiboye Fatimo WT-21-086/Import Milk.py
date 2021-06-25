{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Project 2: Exploring the Uganda's milk imports and exports\n",
    "A country's economy depends, sometimes heavily, on its exports and imports. The United Nations Comtrade database provides data on global trade. It will be used to analyse the Uganda's imports and exports of milk in 2015:\n",
    "\n",
    "* How much does the Uganda export and import and is the balance positive (more exports than imports)?\n",
    "* Which are the main trading partners, i.e. from/to which countries does the Uganda import/export the most?\n",
    "* Which are the regular customers, i.e. which countries buy milk from the Uganda every month?\n",
    "* Which countries does the Uganda both import from and export to?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import warnings\n",
    "warnings.simplefilter('ignore', FutureWarning)\n",
    "\n",
    "from pandas import *\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Getting and preparing the data\n",
    "\n",
    "The data is obtained from the [United Nations Comtrade](http://comtrade.un.org/data/) website, by selecting the following configuration:\n",
    "\n",
    "- Type of Product: goods\n",
    "- Frequency: monthly \n",
    "- Periods: Jan - May 2018\n",
    "- Reporter: Uganda\n",
    "- Partners: all\n",
    "- Flows: imports and exports\n",
    "- HS (as reported) commodity codes: 401 (Milk and cream, neither concentrated nor sweetened) and 402 (Milk and cream, concentrated or sweetened)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "LOCATION = 'comrade_milk_ug_jan_dec_2015.csv'"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "On reading in the data, the commodity code has to be read as a string, to not lose the leading zero."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Classification</th>\n",
       "      <th>Year</th>\n",
       "      <th>Period</th>\n",
       "      <th>Period Desc.</th>\n",
       "      <th>Aggregate Level</th>\n",
       "      <th>Is Leaf Code</th>\n",
       "      <th>Trade Flow Code</th>\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Reporter Code</th>\n",
       "      <th>Reporter</th>\n",
       "      <th>...</th>\n",
       "      <th>Qty</th>\n",
       "      <th>Alt Qty Unit Code</th>\n",
       "      <th>Alt Qty Unit</th>\n",
       "      <th>Alt Qty</th>\n",
       "      <th>Netweight (kg)</th>\n",
       "      <th>Gross weight (kg)</th>\n",
       "      <th>Trade Value (US$)</th>\n",
       "      <th>CIF Trade Value (US$)</th>\n",
       "      <th>FOB Trade Value (US$)</th>\n",
       "      <th>Flag</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>289</td>\n",
       "      <td>HS</td>\n",
       "      <td>2015</td>\n",
       "      <td>201512</td>\n",
       "      <td>Dec-15</td>\n",
       "      <td>4</td>\n",
       "      <td>0</td>\n",
       "      <td>2</td>\n",
       "      <td>Exports</td>\n",
       "      <td>800</td>\n",
       "      <td>Uganda</td>\n",
       "      <td>...</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>3000.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>991</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>290</td>\n",
       "      <td>HS</td>\n",
       "      <td>2015</td>\n",
       "      <td>201512</td>\n",
       "      <td>Dec-15</td>\n",
       "      <td>4</td>\n",
       "      <td>0</td>\n",
       "      <td>2</td>\n",
       "      <td>Exports</td>\n",
       "      <td>800</td>\n",
       "      <td>Uganda</td>\n",
       "      <td>...</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>18930.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>56999</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2 rows × 35 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "    Classification  Year  Period Period Desc.  Aggregate Level  Is Leaf Code  \\\n",
       "289             HS  2015  201512       Dec-15                4             0   \n",
       "290             HS  2015  201512       Dec-15                4             0   \n",
       "\n",
       "     Trade Flow Code Trade Flow  Reporter Code Reporter  ...  Qty  \\\n",
       "289                2    Exports            800   Uganda  ...  NaN   \n",
       "290                2    Exports            800   Uganda  ...  NaN   \n",
       "\n",
       "     Alt Qty Unit Code Alt Qty Unit  Alt Qty  Netweight (kg)  \\\n",
       "289                NaN          NaN      NaN          3000.0   \n",
       "290                NaN          NaN      NaN         18930.0   \n",
       "\n",
       "     Gross weight (kg)  Trade Value (US$)  CIF Trade Value (US$)  \\\n",
       "289                NaN                991                    NaN   \n",
       "290                NaN              56999                    NaN   \n",
       "\n",
       "     FOB Trade Value (US$)  Flag  \n",
       "289                    NaN     0  \n",
       "290                    NaN     0  \n",
       "\n",
       "[2 rows x 35 columns]"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "milk = pd.read_csv(LOCATION, dtype={'Commodity Code':str})\n",
    "milk.tail(2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The data only covers the first five months of 2015. Most columns are irrelevant for this analysis, or contain always the same value, like the year and reporter columns. The commodity code is transformed into a short but descriptive text and only the relevant columns are selected."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Period</th>\n",
       "      <th>Partner</th>\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Milk and cream</th>\n",
       "      <th>Trade Value (US$)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>0</td>\n",
       "      <td>201501</td>\n",
       "      <td>World</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>3671</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>1</td>\n",
       "      <td>201501</td>\n",
       "      <td>World</td>\n",
       "      <td>Exports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>473724</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>201501</td>\n",
       "      <td>Burundi</td>\n",
       "      <td>Exports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>19996</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>201501</td>\n",
       "      <td>Denmark</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>1234</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>201501</td>\n",
       "      <td>France</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>715</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Period  Partner Trade Flow Milk and cream  Trade Value (US$)\n",
       "0  201501    World    Imports    unprocessed               3671\n",
       "1  201501    World    Exports    unprocessed             473724\n",
       "2  201501  Burundi    Exports    unprocessed              19996\n",
       "3  201501  Denmark    Imports    unprocessed               1234\n",
       "4  201501   France    Imports    unprocessed                715"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def milkType(code):\n",
    "    if code == '401': # neither concentrated nor sweetened\n",
    "        return 'unprocessed'\n",
    "    if code == '402': # concentrated or sweetened\n",
    "        return 'processed' \n",
    "    return 'unknown'\n",
    "\n",
    "COMMODITY = 'Milk and cream'\n",
    "milk[COMMODITY] = milk['Commodity Code'].apply(milkType)\n",
    "MONTH = 'Period'\n",
    "PARTNER = 'Partner'\n",
    "FLOW = 'Trade Flow'\n",
    "VALUE = 'Trade Value (US$)'\n",
    "headings = [MONTH, PARTNER, FLOW, COMMODITY, VALUE]\n",
    "milk = milk[headings]\n",
    "milk.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The data contains the total imports and exports per month, under the 'World' partner. Those rows are removed to keep only the per-country data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Period</th>\n",
       "      <th>Partner</th>\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Milk and cream</th>\n",
       "      <th>Trade Value (US$)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>2</td>\n",
       "      <td>201501</td>\n",
       "      <td>Burundi</td>\n",
       "      <td>Exports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>19996</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>3</td>\n",
       "      <td>201501</td>\n",
       "      <td>Denmark</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>1234</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>4</td>\n",
       "      <td>201501</td>\n",
       "      <td>France</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>715</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>5</td>\n",
       "      <td>201501</td>\n",
       "      <td>Rwanda</td>\n",
       "      <td>Exports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>89479</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>6</td>\n",
       "      <td>201501</td>\n",
       "      <td>South Africa</td>\n",
       "      <td>Imports</td>\n",
       "      <td>unprocessed</td>\n",
       "      <td>242</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Period       Partner Trade Flow Milk and cream  Trade Value (US$)\n",
       "2  201501       Burundi    Exports    unprocessed              19996\n",
       "3  201501       Denmark    Imports    unprocessed               1234\n",
       "4  201501        France    Imports    unprocessed                715\n",
       "5  201501        Rwanda    Exports    unprocessed              89479\n",
       "6  201501  South Africa    Imports    unprocessed                242"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "milk = milk[milk[PARTNER] != 'World']\n",
    "milk.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Period</th>\n",
       "      <th>Partner</th>\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Milk and cream</th>\n",
       "      <th>Trade Value (US$)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>285</td>\n",
       "      <td>201512</td>\n",
       "      <td>United Rep. of Tanzania</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>24300</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>286</td>\n",
       "      <td>201512</td>\n",
       "      <td>South Sudan</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>8064</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>287</td>\n",
       "      <td>201512</td>\n",
       "      <td>Rwanda</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>64025</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>289</td>\n",
       "      <td>201512</td>\n",
       "      <td>Burundi</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>991</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>290</td>\n",
       "      <td>201512</td>\n",
       "      <td>Dem.Rep. of the Congo</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>56999</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "     Period                  Partner Trade Flow Milk and cream  \\\n",
       "285  201512  United Rep. of Tanzania    Exports      processed   \n",
       "286  201512              South Sudan    Exports      processed   \n",
       "287  201512                   Rwanda    Exports      processed   \n",
       "289  201512                  Burundi    Exports      processed   \n",
       "290  201512    Dem.Rep. of the Congo    Exports      processed   \n",
       "\n",
       "     Trade Value (US$)  \n",
       "285              24300  \n",
       "286               8064  \n",
       "287              64025  \n",
       "289                991  \n",
       "290              56999  "
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "milk.tail()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Total trade flow\n",
    "To answer the first question, 'how much does the Uganda export and import and is the balance positive (more exports than imports)?', the dataframe is split into two groups: exports from the Uganda and imports into the Uganda. The trade values within each group are summed up to get the total trading."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Trade Flow\n",
       "Exports    35275160\n",
       "Imports     2259310\n",
       "Name: Trade Value (US$), dtype: int64"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "grouped = milk.groupby([FLOW])\n",
    "grouped[VALUE].aggregate(sum)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This shows a trade surplus of over 30 million dollars."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Main trade partners\n",
    "\n",
    "To address the second question, 'Which are the main trading partners, i.e. from/to which countries does the Uganda import/export the most?', the dataframe is split by country instead, and then each group aggregated for the total trade value. This is done separately for imports and exports. The result is sorted in descending order so that the main partners are at the top."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The Uganda imports from 24 countries.\n",
      "The 5 biggest exporters to the Uganda are:\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "Partner\n",
       "Kenya                   1020463\n",
       "Netherlands              411429\n",
       "United Arab Emirates     243939\n",
       "Oman                     199876\n",
       "South Africa             126118\n",
       "Name: Trade Value (US$), dtype: int64"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "imports = milk[milk[FLOW] == 'Imports']\n",
    "grouped = imports.groupby([PARTNER])\n",
    "print('The Uganda imports from', len(grouped), 'countries.')\n",
    "print('The 5 biggest exporters to the Uganda are:')\n",
    "totalImports = grouped[VALUE].aggregate(sum).sort_values(inplace=False,ascending=False)\n",
    "totalImports.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The export values can be plotted as a bar chart, making differences between countries easier to see."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x1c3c850eac8>"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "totalImports.head(10).plot(kind='barh')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can deduce that Switzerland is the lowest partnering company of milk to Uganda for imports."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The Uganda exports to 10 countries.\n",
      "The 5 biggest importers from the Uganda are:\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "Partner\n",
       "Kenya                      30237033\n",
       "South Sudan                 2533575\n",
       "Rwanda                       869466\n",
       "United Rep. of Tanzania      533366\n",
       "Japan                        446596\n",
       "Name: Trade Value (US$), dtype: int64"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "exports = milk[milk[FLOW] == 'Exports']\n",
    "grouped = exports.groupby([PARTNER])\n",
    "print('The Uganda exports to', len(grouped), 'countries.')\n",
    "print('The 5 biggest importers from the Uganda are:')\n",
    "grouped[VALUE].aggregate(sum).sort_values(ascending=False,inplace=False).head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Regular importers\n",
    "\n",
    "Given that there are two commodities, the third question, 'Which are the regular customers, i.e. which countries buy milk from the Uganda every month?', is meant in the sense that a regular customer imports both commodities every month. This means that if the exports dataframe is grouped by country, each group has exactly ten rows (two commodities bought each of the five months). To see the countries, only the first month of one commodity has to be listed, as by definition it's the same countries every month and for the other commodity."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "     Period Partner Trade Flow Milk and cream  Trade Value (US$)\n",
      "5    201501  Rwanda    Exports    unprocessed              89479\n",
      "15   201502  Rwanda    Exports    unprocessed              40316\n",
      "28   201501  Rwanda    Exports      processed              28170\n",
      "30   201501   Kenya    Exports      processed             164116\n",
      "46   201502  Rwanda    Exports      processed               9870\n",
      "53   201503   Kenya    Exports    unprocessed             427005\n",
      "54   201503  Rwanda    Exports    unprocessed              60944\n",
      "62   201504   Kenya    Exports    unprocessed             164518\n",
      "65   201504  Rwanda    Exports    unprocessed              55548\n",
      "81   201503   Kenya    Exports      processed            2889812\n",
      "93   201504  Rwanda    Exports      processed               8794\n",
      "96   201504   Kenya    Exports      processed             491255\n",
      "102  201505   Kenya    Exports    unprocessed             823719\n",
      "104  201505  Rwanda    Exports    unprocessed              51333\n",
      "115  201506   Kenya    Exports    unprocessed            1329559\n",
      "117  201506  Rwanda    Exports    unprocessed              58566\n",
      "133  201505   Kenya    Exports      processed            4121189\n",
      "134  201505  Rwanda    Exports      processed             105002\n",
      "145  201506  Rwanda    Exports      processed               1898\n",
      "146  201506   Kenya    Exports      processed            4838396\n",
      "153  201507   Kenya    Exports    unprocessed            1588589\n",
      "154  201507  Rwanda    Exports    unprocessed              12670\n",
      "163  201508   Kenya    Exports    unprocessed            1347178\n",
      "164  201508  Rwanda    Exports    unprocessed              77258\n",
      "180  201507   Kenya    Exports      processed            4975538\n",
      "181  201507  Rwanda    Exports      processed              32000\n",
      "193  201508   Kenya    Exports      processed            1569400\n",
      "199  201509   Kenya    Exports    unprocessed             708175\n",
      "200  201509  Rwanda    Exports    unprocessed              46005\n",
      "212  201509   Kenya    Exports      processed            1748002\n",
      "223  201510   Kenya    Exports    unprocessed             748874\n",
      "224  201510  Rwanda    Exports    unprocessed              39260\n",
      "240  201510   Kenya    Exports      processed             313792\n",
      "247  201511   Kenya    Exports    unprocessed             691882\n",
      "248  201511  Rwanda    Exports    unprocessed              43399\n",
      "260  201511  Rwanda    Exports      processed               2364\n",
      "261  201511   Kenya    Exports      processed             624220\n",
      "270  201512   Kenya    Exports    unprocessed             671814\n",
      "271  201512  Rwanda    Exports    unprocessed              42565\n",
      "287  201512  Rwanda    Exports      processed              64025\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Period</th>\n",
       "      <th>Partner</th>\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Milk and cream</th>\n",
       "      <th>Trade Value (US$)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>28</td>\n",
       "      <td>201501</td>\n",
       "      <td>Rwanda</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>28170</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>30</td>\n",
       "      <td>201501</td>\n",
       "      <td>Kenya</td>\n",
       "      <td>Exports</td>\n",
       "      <td>processed</td>\n",
       "      <td>164116</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    Period Partner Trade Flow Milk and cream  Trade Value (US$)\n",
       "28  201501  Rwanda    Exports      processed              28170\n",
       "30  201501   Kenya    Exports      processed             164116"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def buysEveryMonth(group):\n",
    "    reply = len(group) == 20\n",
    "    return reply\n",
    "\n",
    "grouped = exports.groupby([PARTNER])\n",
    "regular = grouped.filter(buysEveryMonth)\n",
    "print(regular)\n",
    "regular[(regular[MONTH] == 201501) & (regular[COMMODITY] == 'processed')]\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Just over 5% of the total Uganda exports are due to these regular customers."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.8818244623128569"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "regular[VALUE].sum() / exports[VALUE].sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Bi-directional trade\n",
    "\n",
    "To address the fourth question, \n",
    "'Which countries does the Uganda both import from and export to?', a pivot table is used to list the total export and import value for each country. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Exports</th>\n",
       "      <th>Imports</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Partner</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>Australia</td>\n",
       "      <td>NaN</td>\n",
       "      <td>17.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Burundi</td>\n",
       "      <td>262905.0</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>China</td>\n",
       "      <td>NaN</td>\n",
       "      <td>5179.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Dem.Rep. of the Congo</td>\n",
       "      <td>188248.0</td>\n",
       "      <td>48.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Denmark</td>\n",
       "      <td>NaN</td>\n",
       "      <td>3780.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Trade Flow              Exports  Imports\n",
       "Partner                                 \n",
       "Australia                   NaN     17.0\n",
       "Burundi                262905.0      NaN\n",
       "China                       NaN   5179.0\n",
       "Dem.Rep. of the Congo  188248.0     48.0\n",
       "Denmark                     NaN   3780.0"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "countries = pivot_table(milk, index=[PARTNER], columns=[FLOW], \n",
    "                        values=VALUE, aggfunc=sum)\n",
    "countries.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Removing the rows with a missing value will result in only those countries with bi-directional trade flow with the Uganda."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>Trade Flow</th>\n",
       "      <th>Exports</th>\n",
       "      <th>Imports</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Partner</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>Dem.Rep. of the Congo</td>\n",
       "      <td>188248.0</td>\n",
       "      <td>48.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Kenya</td>\n",
       "      <td>30237033.0</td>\n",
       "      <td>1020463.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Rwanda</td>\n",
       "      <td>869466.0</td>\n",
       "      <td>3096.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>United Arab Emirates</td>\n",
       "      <td>90939.0</td>\n",
       "      <td>243939.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>United Rep. of Tanzania</td>\n",
       "      <td>533366.0</td>\n",
       "      <td>65472.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Trade Flow                  Exports    Imports\n",
       "Partner                                       \n",
       "Dem.Rep. of the Congo      188248.0       48.0\n",
       "Kenya                    30237033.0  1020463.0\n",
       "Rwanda                     869466.0     3096.0\n",
       "United Arab Emirates        90939.0   243939.0\n",
       "United Rep. of Tanzania    533366.0    65472.0"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "countries.dropna()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Conclusions\n",
    "\n",
    "The milk and cream trade of the Uganda from January to December 2015 was analysed in terms of which countries the Uganda mostly depends on for income (exports) and goods (imports). Over the period, the Uganda had a trade surplus of over 1 million US dollars.\n",
    "\n",
    "Kenya is the main partner, but it exported from the Uganda almost the triple in value than it imported to the Uganda. \n",
    "\n",
    "The Uganda exported to over 100 countries during the period, but only imported from 24 countries, the main ones (top five by trade value) being not so geographically close (Kenya, Netherlands, United Arab Emirates, Oman, and South Africa). Kenya and Netherlands are the main importers that are not also main exporters except Kenya. \n",
    "\n",
    "The Uganda is heavily dependent on its regular customers, the 10 countries that buy all types of milk and cream every month. They contribute three quarters of the total export value.\n",
    "\n",
    "Although for some, the trade value (in US dollars) is suspiciously low, which raises questions about the data's accuracy.\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}